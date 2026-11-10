import json
from pathlib import Path

STATE_FILE = Path(__file__).resolve().parent / "state.json"   # main.py와 같은 폴더의 state.json

def get_number(prompt, min_val, max_val):
    while True:                             #올바른 입력까지 계속 반복
        user_input = input(prompt).strip()  #앞 뒤 공백 제거

        if user_input == "":                #빈 입력 체크
            print("입력이 비어있습니다. 다시 입력해주세요. 🙏")
            continue

        try:
            number = int(user_input)        #숫자로 변환 시도
        except ValueError:                  #abc처럼 변환할 수 없으면
            print("숫자만 입력해주세요! 🔢")
            continue

        number = int(user_input)            #숫자로 변환

        if number < min_val or number > max_val:
            print(f"{min_val}~{max_val} 사이로 입력해주세요! 😊")
            continue

        return number                       #올바른 입력이면 숫자 반환


def get_text(prompt):
    while True:                             #올바른 입력까지 계속 반복
        text = input(prompt).strip()        #앞뒤 공백 제거
        if text == "":                      #빈 입력 체크
            print("입력이 비어있습니다. 다시 입력해주세요. 🙏")
            continue
        return text                         #내용이 있으면 반환

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

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    @staticmethod
    def from_dict(data):
        return Quiz(
            data["question"],
            data["choices"],
            data["answer"]
        )

# 기본 퀴즈 5개 만들기 (틀로 찍어내기!)
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
        self.best_score = 0 # 최고 점수
        self.load() # 시작할 때 불러오기

    def show_menu(self):
        print("\n==== 퀴즈 게임 ====")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("0. 종료")

    def run(self):
        try:
            while True:             # 계속 반복
                self.show_menu()
                choice = get_number("원하는 번호를 고르세요: ", 0, 4) #공백/빈칸/문자/범위 검증
                if choice == 0:
                    print("게임을 종료합니다! 👋")
                    break               #반복 멈추기
                elif choice == 1:
                    self.play_quiz()      #퀴즈 풀기 실행
                elif choice == 2:
                    self.add_quiz()       #퀴즈 추가 실행       
                elif choice == 3:
                    self.show_list()
                elif choice == 4:
                    self.show_score()
        except (KeyboardInterrupt, EOFError):
            print("\n\n입력이 중단되어 게임을 안전하게 종료합니다. 💾")
            self.save()              #종료 전 저장
            
    def play_quiz(self):
        if not self.quizzes:
            print("풀 수 있는 퀴즈가 없어요! 😢")
            return
        
        score = 0
        for quiz in self.quizzes:
            quiz.show()
            답 = get_number("정답 번호를 입력하세요: ", 1, 4)
            if quiz.is_correct(user_answer):
                print("정답입니다! 🎉")
                score = score + 1
            else:
                print("틀렸습니다! 😢")
        print(f"\n최종 점수: {score} / {len(self.quizzes)}")

        if score > self.best_score:
            self.best_score = score
            print("🏆 최고 점수를 갱신했어요!")
            self.save()                 #점수 갱신 후 저장

    def show_list(self):
        if not self.quizzes:                                  #퀴즈가 하나도 없으면
            print("등록된 퀴즈가 없어요! 😢")
            return
        print(f"\n=== 퀴즈 목록 (총 {len(self.quizzes)}개) ===")
        for num, quiz in enumerate(self.quizzes, 1):          #1번부터 번호 붙이기
            print(f"[{num}] {quiz.question}")

    def show_score(self):
        if self.best_score == 0:                              #아직 기록이 없으면
            print("\n아직 퀴즈를 푼 기록이 없어요! 먼저 퀴즈를 풀어보세요. 📝")
            return
        print(f"\n🏆 최고 점수: {self.best_score}문제 정답")

    def add_quiz(self):
        print("\n=== 퀴즈 추가 ===")

        question = get_text("문제를 입력하세요: ")            #문제받기

        choices = []                                       #선택지 담을 빈 리스트
        for i in range(1, 5):                              #1.2.3.4 네 번 반복
            choice = get_text(f"{i}번 선택지: ")           #선택지(빈 입력 방지)
            choices.append(choice)                         #리스트에 하나씩 추가

        answer = get_number("정답 번호(1~4): ", 1, 4)       #정답 받기(검증까지)

        new_quiz = Quiz(question, choices, answer)          #Quiz 만들기
        self.quizzes.append(new_quiz)                       #퀴즈 목록에 추가

        print("퀴즈가 추가되었어요! 🎉")
        self.save()                                         #추가 후 저장
    
    def save(self):
        data = {                                             #모든 퀴즈를 딕셔너리로 변환
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:  #파일에 저장(UTF-8로 한글 깨짐 방지)
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError:                                      #쓰기 오류(권한 없음, 디스크 문제 등)
            print("⚠️ 파일 저장 중 오류가 발생했어요. 이번 변경은 저장되지 않았습니다.")

    def load(self):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.quizzes = [Quiz.from_dict(d) for d in data["quizzes"]]
            self.best_score = data["best_score"]
            print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고 점수 {self.best_score})")

        except FileNotFoundError:                            #파일이 없을 때(첫 실행)
            print("저장된 파일이 없어 기본 퀴즈로 시작합니다.")
            self.quizzes = get_default_quizzes()

        except (json.JSONDecodeError, KeyError, TypeError):  #파일 내용이 손상됐을 때
            print("파일이 손상되어 기본 퀴즈로 복구합니다.")
            self.quizzes = get_default_quizzes()

        except OSError:                                      #그 밖의 읽기 오류
            print("파일을 읽을 수 없어 기본 퀴즈로 시작합니다.")
            self.quizzes = get_default_quizzes()

if __name__ == "__main__":
    game = QuizGame() # 게임 만들기
    game.run() # 게임 실행!
