from flask import Flask, render_template, request, redirect, url_for, session
import random
import json
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

# 공백 제거 함수
def clean_text(text):
    return text.strip() if isinstance(text, str) else text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_questions():
    json_path = os.path.join(BASE_DIR, 'questions.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# ✅ 로그인 필요 데코레이터
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == os.environ.get('ACCESS_PASSWORD', '8104'):  # Render에서 설정
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="비밀번호가 올바르지 않습니다.")
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

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
