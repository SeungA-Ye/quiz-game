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

# 문제 보여주기!
quiz1.show()
quiz2.show()
quiz3.show()
