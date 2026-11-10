class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question # 문제
        self.choices = choices # 선택지 4개 (리스트)
        self.answer = answer # 정답 번호 (1~4)

    def show(self):
        print(self.question)
        for i, choice in enumerate(self.choices, 1):
            print(f"{i}. {choice}")

    def is_correct(self, user_input):
        return self.answer == user_input

# 문제 3개 만들기 (틀로 찍어내기!)
def get_default_quizzes():
    quiz1 = Quiz(
        "지구에 사는 동물 가운데 가장 큰 동물은?",
        ["대왕고래","아프리카코끼리","고래상어","향유고래"],
        1
        )

    quiz2 = Quiz(
        "땅 위에서 가장 빨리 달리는 동물은?",
        ["사자","캥거루","얼룩말","치타"],
        4
        )

    quiz3 = Quiz(
        "땅 위에 사는 동물 가운데 키가 가장 큰 동물은?",
        ["낙타","기린","코끼리","타조"],
        2
        )

    quiz4 = Quiz(
        "꿀을 만드는 곤충은?",
        ["벌","잠자리","메뚜기","여치"],
        1
        )

    quiz5 = Quiz(
        "날개가 있지만 날지 못하는 새는?",
        ["참새","벌새","기러기","닭"],
        4
        )
    return [quiz1, quiz2, quiz3, quiz4, quiz5]

quizzes = get_default_quizzes()

for quiz in quizzes:
    quiz.show()
    답 = input("정답 번호를 입력하세요: ")
    if quiz.is_correct(int(답)):
        print("정답입니다! 🎉")
    else:
        print("틀렸습니다! 😢")
