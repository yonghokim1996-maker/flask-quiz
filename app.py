from flask import Flask, render_template, request
import random
import json
import os

app = Flask(__name__)

# 공백 제거 함수
def clean_text(text):
    return text.strip() if isinstance(text, str) else text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_questions():
    json_path = os.path.join(BASE_DIR, 'questions.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def index():
    questions = load_questions()
    randomized_questions = []

    # 질문을 셔플하면서 원본 인덱스를 함께 저장
    indexed_questions = list(enumerate(questions))
    random.shuffle(indexed_questions)

    for original_index, q in indexed_questions:
        shuffled_choices = q['choices'][:]
        random.shuffle(shuffled_choices)
        randomized_questions.append({
            "id": original_index,  # 원본 인덱스 저장
            "question": clean_text(q['question']),
            "choices": [clean_text(c) for c in shuffled_choices],
            "image": q.get('image'),
            "answer": clean_text(q['answer']),
            "explanation": q.get('explanation', '해설이 준비되지 않았습니다.')
        })

    return render_template('index.html', questions=randomized_questions)

@app.route('/submit', methods=['POST'])
def submit():
    questions = load_questions()
    score = 0
    incorrect_answers = []

    # 원본 질문 인덱스를 사용해서 정확하게 매칭
    for q in questions:
        q_id = questions.index(q)
        user_answer = request.form.get(f'q{q_id}')
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

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
