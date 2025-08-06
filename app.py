from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import random
import json
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, 'questions.json')

def clean_text(text):
    return text.strip() if isinstance(text, str) else text

def load_questions():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_questions(questions):
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

# 로그인 데코레이터
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# 관리자 전용 데코레이터
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# 사용자 로그인
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == os.environ.get('USER_PASSWORD', '8104'):
            session['user_logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="비밀번호가 올바르지 않습니다.")
    return render_template('login.html')

# 관리자 로그인
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == os.environ.get('ADMIN_PASSWORD', '2241'):
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('login.html', error="관리자 비밀번호가 올바르지 않습니다.")
    return render_template('login.html')

@app.route('/')
@login_required
def index():
    questions = load_questions()
    randomized_questions = []

    shuffled_questions = questions[:]
    random.shuffle(shuffled_questions)

    for q in shuffled_questions:
        shuffled_choices = q['choices'][:]
        random.shuffle(shuffled_choices)
        randomized_questions.append({
            "question": clean_text(q['question']),
            "choices": [clean_text(c) for c in shuffled_choices],
            "image": q.get('image'),
            "answer": clean_text(q['answer']),
            "explanation": q.get('explanation', '해설이 준비되지 않았습니다.')
        })

    return render_template('index.html', questions=randomized_questions)

@app.route('/submit', methods=['POST'])
@login_required
def submit():
    questions = load_questions()
    score = 0
    incorrect_answers = []

    for i, q in enumerate(questions):
        user_answer = request.form.get(f'q{i}')
        if user_answer and clean_text(user_answer) == clean_text(q['answer']):
            score += 1
        else:
            incorrect_answers.append({
                "question": q['question'],
                "your_answer": user_answer if user_answer else "미응답",
                "correct_answer": q['answer'],
                "explanation": q.get('explanation', '해설이 준비되지 않았습니다.')
            })

    return render_template('result.html',
                           score=score,
                           total=len(questions),
                           incorrect_answers=incorrect_answers)

# 관리자 대시보드
@app.route('/admin')
@admin_required
def admin_dashboard():
    questions = load_questions()
    return render_template('admin_dashboard.html', questions=questions)

# 문제 수정
@app.route('/admin/edit/<int:index>', methods=['POST'])
@admin_required
def edit_question(index):
    questions = load_questions()
    questions[index] = {
        "question": request.form['question'],
        "choices": request.form.getlist('choices'),
        "answer": request.form['answer'],
        "explanation": request.form.get('explanation', '')
    }
    save_questions(questions)
    return redirect(url_for('admin_dashboard'))

# 문제 추가
@app.route('/admin/add', methods=['POST'])
@admin_required
def add_question():
    questions = load_questions()
    new_question = {
        "question": request.form['question'],
        "choices": request.form.getlist('choices'),
        "answer": request.form['answer'],
        "explanation": request.form.get('explanation', '')
    }
    questions.append(new_question)
    save_questions(questions)
    return redirect(url_for('admin_dashboard'))

# 문제 삭제
@app.route('/admin/delete/<int:index>', methods=['POST'])
@admin_required
def delete_question(index):
    questions = load_questions()
    if 0 <= index < len(questions):
        questions.pop(index)
        save_questions(questions)
    save_questions(questions)
    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
