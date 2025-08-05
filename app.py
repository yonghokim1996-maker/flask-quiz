from flask import Flask, render_template, request, redirect, url_for, session
import random
import json
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def clean_text(text):
    return text.strip() if isinstance(text, str) else text

def load_questions():
    json_path = os.path.join(BASE_DIR, 'questions.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# ✅ 로그인 데코레이터
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ✅ 관리자 전용 데코레이터
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# 🔑 일반 사용자 로그인
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

# 🔑 관리자 로그인
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == os.environ.get('ADMIN_PASSWORD', '2241'):
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error="관리자 비밀번호가 올바르지 않습니다.")
    return render_template('login.html')

@app.route('/')
@login_required
def index():
    questions = load_questions()
    randomized_questions = []

    # 질문 섞기
    shuffled = list(enumerate(questions))
    random.shuffle(shuffled)

    for idx, q in shuffled:
        shuffled_choices = q['choices'][:]
        random.shuffle(shuffled_choices)
        randomized_questions.append({
            "id": idx,  # 원본 인덱스 저장
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

    for i in range(len(questions)):
        q_id = request.form.get(f'id{i}')
        if q_id is None:
            continue
        q_id = int(q_id)
        user_answer = request.form.get(f'q{i}')

        correct_answer = clean_text(questions[q_id]['answer'])

        if user_answer and clean_text(user_answer) == correct_answer:
            score += 1
        else:
            incorrect_answers.append({
                "question": questions[q_id]['question'],
                "your_answer": user_answer if user_answer else "미응답",
                "correct_answer": correct_answer,
                "explanation": questions[q_id].get('explanation', '해설이 준비되지 않았습니다.')
            })

    return render_template('result.html',
                           score=score,
                           total=len(questions),
                           incorrect_answers=incorrect_answers)

@app.route('/admin')
@admin_required
def admin():
    return "여기서 문제를 수정/추가/삭제할 수 있는 페이지를 만들면 됩니다."

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
