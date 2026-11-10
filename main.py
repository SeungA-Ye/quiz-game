def get_number(prompt, min_val, max_val):
    while True:                             #올바른 입력까지 계속 반복
        user_input = input(prompt).strip()  #앞 뒤 공백 제거

        if user_input == "":                #빈 입력 체크
            print("입력이 비어있습니다. 다시 입력해주세요. 🙏")
            continue

        if not user_input.isdigit():        #숫자가 아니면
            print("숫자만 입력해주세요! 🔢")
            continue

        number = int(user_input)            #숫자로 변환

        if number < min_val or number > max_val:
            print(f"{min_val}~{max_val} 사이로 입력해주세요! 😊")
            continue

        return number                       #올바른 입력이면 숫자 반환

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
            elif choice == "2":
                self.add_quiz()       #퀴즈 추가 실행       
            elif choice == "3":
                self.show_list()
            elif choice == "4":
                self.show_score()
            else:
                print("없는 번호예요! 다시 골라주세요 🙏")

    def play_quiz(self):
        if not self.quizzes:
            print("풀 수 있는 퀴즈가 없어요! 😢")
            return
        
        score = 0
        for quiz in self.quizzes:
            quiz.show()
            답 = get_number("정답 번호를 입력하세요: ", 1, 4)
            if quiz.is_correct(답):
                print("정답입니다! 🎉")
                score = score + 1
            else:
                print("틀렸습니다! 😢")
        print(f"\n최종 점수: {score} / {len(self.quizzes)}")

        if score > self.best_score:
            self.best_score = score
            print("🏆 최고 점수를 갱신했어요!")


    def show_list(self):
        print("\n=== 퀴즈 목록 ===")
        for quiz in self.quizzes:       #퀴즈 하나씩 꺼내서
            quiz.show()                 #퀴즈 보여주기
            print()                     #문제 사이에 한 줄 띄우기

    def show_score(self):
        print(f"\n🏆 현재 최고 점수: {self.best_score} / {len(self.quizzes)}")

    def add_quiz(self):
        print("\n=== 퀴즈 추가 ===")

        question = input("문제를 입력하세요: ")            #문제받기

        choices = []                                       #선택지 담을 빈 리스트
        for i in range(1, 5):                              #1.2.3.4 네 번 반복
            choice = input(f"{i}번 선택지: ")
            choices.append(choice)                         #리스트에 하나씩 추가

        answer = get_number("정답 번호(1~4): ", 1, 4)       #정답 받기(검증까지)

        new_quiz = Quiz(question, choices, answer)          #Quiz 만들기
        self.quizzes.append(new_quiz)                       #퀴즈 목록에 추가

        print("퀴즈가 추가되었어요! 🎉")

game = QuizGame() # 게임 만들기
game.run() # 게임 실행!
