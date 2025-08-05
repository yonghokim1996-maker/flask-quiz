from flask import Flask, render_template, request
import random

app = Flask(__name__)

# 공백 제거 함수
def clean_text(text):
    return text.strip() if isinstance(text, str) else text

# 샘플 문제 데이터 (전체 공백 제거)
questions = [
    {
        "question": clean_text("CLEAN ROOM에서 지켜야 할 사항 중 아닌것은?"),
        "choices": [clean_text(c) for c in [
            "흡연 및 식음은 할 수 없고 청정실내로 모든 음식 반입은 금지된다.",
            "모든 인원은 무진복 및 무진화를 착용하고 착용시 신체 및 머리카락, 평상복을 충분이 덮어야 한다.",
            "화장품은 허용하지 않으며 헤어 스프레이, 핸드 로션/크림 및 빗은 청정실에서 사용할 수 없다.",
            "무진복은 한달에 한번은 세탁해야 한다."
        ]],
        "answer": clean_text("무진복은 한달에 한번은 세탁해야 한다."),
        "explanation": "무진복은 한 달에 한 번이 아니라 2주에 한번씩 세탁을 진행해야 합니다."
    },
    {
        "question": clean_text("마찰 또는 대전 등에 의해 발생되며, 전자의 과잉이나 결핍으로 전기적 불균형 상태에서 순간적으로 발생하는게 정전기이다"),
        "choices": [clean_text(c) for c in ["O", "X"]],
        "answer": clean_text("O"),
        "explanation": "문제 자체가 정전기의 정의 입니다."
    },
    {
        "question": clean_text("접촉성 대전은 두 물체가 서로 접촉이나 분리시 대전되는 것이고 정전기의 양은 재질의 종류, 근접도, 표면의 거칠기, 접촉하는 압력, 문지름이나 분리되는 속도에 의한다"),
        "choices": [clean_text(c) for c in ["O", "X"]],
        "answer": clean_text("O")
    },
    {
        "question": clean_text("정전기 예방을 위해 인체와 무관한 정전기 방지 물품은?"),
        "choices": [clean_text(c) for c in ["정전기 방지용 무진화", "무진복", "무진장갑", "이오나이저"]],
        "answer": clean_text("이오나이저"),
        "explanation": "이오나이저는 인체의 무관한 정전기 방지 제품 입니다."
    },
    {
        "question": clean_text("정전기의 일반적인 요구사항?"),
        "choices": [clean_text(c) for c in [
            "정전기에 민감한 제품은 규정된 절차에 따라 정전기 방지구역 내에서 취급해야 한다",
            "이오나이저가 사용되는 곳은 작업 중에 항상 켜 놓지 않아두 된다.",
            "롯트 트레블러 카드, 스케쥴과 같은 종이는 정전기 발생방지 재질로 만들어진 봉투에 담아야 한다.",
            "모든 자재는 정전기 방지를 위하여 다른 물질과의 마찰을 피해야 한다."
        ]],
        "answer": clean_text("이오나이저가 사용되는 곳은 작업 중에 항상 켜 놓지 않아두 된다."),
        "explanation": "이오나이저는 항상ㅅ 작업 중에 켜놓아야 합니다."
    },
    {
        "question": clean_text("서류 정정 방법 규정사항 중 아닌것은?"),
        "choices": [clean_text(c) for c in [
            "흰 칠을 하거나 LIQUID를 사용하는 것은 안 된다",
            "연필 사용을 금하며 볼펜을 사용해야 한다.",
            "지워 없애거나 긁어서 없애는 것은 안 된다.",
            "테이프를 붙여두 된다."
        ]],
        "answer": clean_text("테이프를 붙여두 된다."),
        "explanation": "테이프를 절대 붙여서는 안됩니다."
    },
    {
        "question": clean_text("SPC의 필요성 중 맞는것은?"),
        "choices": [clean_text(c) for c in [
            "공정의 변화 폭을 줄여 제품의 품질을 균일하게 하기 위하여",
            "이상점 발생시 필요한 액션을 기간 이내에 취한다.",
            "관리 이탈점이 발생하였을때 바로 조치하지 않아두 된다.",
            "재 작업의 손실방지를 위해 필요하다."
        ]],
        "answer": clean_text("관리 이탈점이 발생하였을때 바로 조치하지 않아두 된다."),
        "explanation": "관리 이탈점이 발생하였을때 바로 조치해야 합니다."
    },
    {
        "question": clean_text("SOLDER PASTE(솔더 페이스트) 성분에 옳은 것은?"),
        "choices": [clean_text(c) for c in [
            "Sn(96.5%) / Ag(3.5%) / Cu(0.5%) -> LEAD(Pb) FREE PASTE",
            "Sn(63%) / Pb(37%)"
        ]],
        "answer": clean_text("Sn(96.5%) / Ag(3.5%) / Cu(0.5%) -> LEAD(Pb) FREE PASTE"),
        "explanation": "Sn(63%) / Pb(37%) -> 유테틱 PASTE 입니다."
    },
    {
        "question": clean_text("솔더 페이스트 보관 및 관리에 아닌것은?"),
        "choices": [clean_text(c) for c in [
            "페이스트는 상온에서 최소 2 시간 해동 후 사용(용기가 개봉된 경우 최대 24 시간동안 사용 가능)",
            "불출된 페이스트는 불출날짜와 시간/폐기날짜와 개봉하기전의 개봉날짜와 시간 기록",
            "PCB 위에 페이스트를 올려놓고 1시간 이내에 리플로우 통과후 볼이 잘 형성되어 양질인지 확인"
        ]],
        "answer": clean_text("PCB 위에 페이스트를 올려놓고 1시간 이내에 리플로우 통과후 볼이 잘 형성되어 양질인지 확인"),
        "explanation": "1시간이 아닌 30분 이내에 리플로우 통과가 되어야 합니다."
    },
    {
        "question": clean_text("SMD Chip Mounting 관련 옳지 않은것은?"),
        "choices": [clean_text(c) for c in [
            "피시비의 표준 로딩 방향으로서 골드 표시가 있는쪽이 작업자 쪽으로 오게 한다.",
            "컴포넌트 밸류 확인은 매 셋업시 마다, 컴포넌트 재로딩시, 그리고 쉽트가 시작될 때마다 진행한다.",
            "리플로우 프로파일은 정비 주임에 의해 매 셋업시 마다 그리고 하루에 한번씩 프로파일러로 취해져야 한다",
            "컴포넌트 밸류 확인은 각 릴당 3개로 진행해야한다."
        ]],
        "answer": clean_text("컴포넌트 밸류 확인은 각 릴당 3개로 진행해야한다."),
        "explanation": "컴포넌트 벨류 확인은 각 릴당 1개로 진행해야 합니다."
    },
    {
        "question": clean_text("산소 농도 PPM은?"),
        "choices": [clean_text(c) for c in ["100PPM", "200PPM", "300PPM", "50PPM"]],
        "answer": clean_text("300PPM"),
        "explanation": "산소 농도는 300PPM 입니다."
    },
    {
        "question": clean_text("클리닝 머신의 장비 셋업 조건 중 다른것은?"),
        "choices": [clean_text(c) for c in [
            "컨베이어 속도 : 15-45inch/min",
            "저장고 온도 : 30-60℃",
            "드라이 온도 : 70-90℃",
            "물저항 : 2 ㏁"
        ]],
        "answer": clean_text("드라이 온도 : 70-90℃"),
        "explanation": "드라이 온도는 70~110℃ 입니다."
    },
    {
        "question": clean_text("아래 이미지는 어떤 불량인지 고르시요?"),
        "image": "T.png",
        "choices": [clean_text(c) for c in [
            "Component tombstone(컴포넌트 툼스톤)",
            "Component Non wet & Dewet(컴포넌트 넌웻 & 디웻)",
            "Component Crack(컴포넌트 크랙)",
            "Missing Component(미씽 컴포넌트)"
        ]],
        "answer": clean_text("Component tombstone(컴포넌트 툼스톤)"),
        "explanation": "툼스톤은 위에서 봤을때 미스얼라인이 약간 있을 경우, 사이드로 봐서 Component 가 약간 들떠 Pad non-wet 이 난 경우 불량이다."
    },
    {
        "question": clean_text("아래 이미지는 어떤 불량인지 고르시요?"),
        "image": "CN.png",
        "choices": [clean_text(c) for c in [
            "Component tombstone(컴포넌트 툼스톤)",
            "Component Non wet & Dewet(컴포넌트 넌웻 & 디웻)",
            "Component Crack(컴포넌트 크랙)",
            "Missing Component(미씽 컴포넌트)"
        ]],
        "answer": clean_text("Component Non wet & Dewet(컴포넌트 넌웻 & 디웻)"),
        "explanation": "Soldering 이 부분적으로 이루어진 경우는 양에 상관없이 불량이다."
    },
    {
        "question": clean_text("아래 이미지는 어떤 불량인지 고르시요?"),
        "image": "CC.png",
        "choices": [clean_text(c) for c in [
            "Component tombstone(컴포넌트 툼스톤)",
            "Component Non wet & Dewet(컴포넌트 넌웻 & 디웻)",
            "Component Crack(컴포넌트 크랙)",
            "Missing Component(미씽 컴포넌트)"
        ]],
        "answer": clean_text("Component Crack(컴포넌트 크랙)"),
        "explanation": "10x 스코프로 위에서 봤을때 표면에 크랙 자국이 있는 경우 불량이다."
        
    },
    {
        "question": clean_text("아래 이미지는 어떤 불량인지 고르시요?"),
        "image": "CM.png",
        "choices": [clean_text(c) for c in [
            "Component tombstone(컴포넌트 툼스톤)",
            "Component Non wet & Dewet(컴포넌트 넌웻 & 디웻)",
            "Component Crack(컴포넌트 크랙)",
            "Missing Component(미씽 컴포넌트)"
        ]],
        "answer": clean_text("Missing Component(미씽 컴포넌트)"),
        "explanation": "Component 가 지정 Pad 위에 빠짐이 발생한 경우 불량이다."
    },
    {
        "question": clean_text("아래 이미지는 어떤 불량인지 고르시요?"),
        "image": "CMA.png",
        "choices": [clean_text(c) for c in [
            "Component tombstone(컴포넌트 툼스톤)",
            "Component Misalignment(컴포넌트 미스얼라인먼트)",
            "Component Crack(컴포넌트 크랙)",
            "Missing Component(미씽 컴포넌트)"
        ]],
        "answer": clean_text("Component Misalignment(컴포넌트 미스얼라인먼트)"),
        "explanation": "Component to Pad 대비 커버율이 25% 미만일 경우 불량이다."
    },
    {
        "question": clean_text("아래 이미지는 어떤 불량인지 고르시요?"),
        "image": "CS2.png",
        "choices": [clean_text(c) for c in [
            "Component Short(컴포넌트 쇼트)",
            "Component Misalignment(컴포넌트 미스얼라인먼트)",
            "Component Crack(컴포넌트 크랙)",
            "Missing Component(미씽 컴포넌트)"
        ]],
        "answer": clean_text("Component Short(컴포넌트 쇼트)"),
        "explanation": "Non-Common net 에서 Solder Paste 로 인해 Short 가 있을 경우 불량이다."
    },
    {
        "question": clean_text("아래 이미지는 어떤 불량인지 고르시요?"),
        "image": "SB.png",
        "choices": [clean_text(c) for c in ["범프 홀", "솔더 브릿지", "범프 크랙", "다이 크랙"]],
        "answer": clean_text("솔더 브릿지")
    },
]

@app.route('/')
def index():
    randomized_questions = []

    shuffled_questions = questions[:]
    random.shuffle(shuffled_questions)

    for q in shuffled_questions:
        shuffled_choices = q['choices'][:]
        random.shuffle(shuffled_choices)
        randomized_questions.append({
            "question": q['question'],
            "choices": shuffled_choices,
            "image": q.get('image'),
            "answer": q['answer'],
            "explanation": q.get('explanation', '해설이 준비되지 않았습니다.')
        })

    return render_template('index.html', questions=list(enumerate(randomized_questions)))

@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    incorrect_answers = []

    shuffled_questions = questions[:]
    for i, q in enumerate(shuffled_questions):
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

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)