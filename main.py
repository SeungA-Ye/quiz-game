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

class QuizGame:
    def __init__(self):
        self.quizzes = get_default_quizzes() #퀴즈 5개 담기
        self.best_score = 0 # 최고 점수

    def show_menu(self):
        print("\n==== 퀴즈 게임 ====")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("0. 종료")

    def run(self):
        while True:             # 계속 반복
            self.show_menu()
            choice = input("원하는 번호를 고르세요: ")
            if choice == "0":
                print("게임을 종료합니다! 👋")
                break               #반복 멈추기
            elif choice == "1":
                self.play_quiz()      #퀴즈 풀기 실행

    def play_quiz(self):
        score = 0
        for quiz in self.quizzes:
            quiz.show()
            답 = input("정답 번호를 입력하세요: ")
            if quiz.is_correct(int(답)):
                print("정답입니다! 🎉")
                score = score + 1
            else:
                print("틀렸습니다! 😢")
        print(f"\n최종 점수: {score} / {len(self.quizzes)}")



game = QuizGame() # 게임 만들기
game.run() # 게임 실행!
