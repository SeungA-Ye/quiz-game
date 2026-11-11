# 🐾 동물 퀴즈 게임

동물에 대한 다양한 상식을 퀴즈로 풀어보는 **터미널(콘솔) 게임**입니다.
Python 기본 문법과 클래스(`Quiz`, `QuizGame`)로 구현했고, 퀴즈와 최고 점수는 `state.json`에 저장되어 프로그램을 다시 실행해도 유지됩니다.

## 📌 주제 선정 이유

동물은 누구에게나 **친숙한 주제**라서, 남녀노소 누구나 부담 없이 즐길 수 있을 것 같아 선택했습니다. 🐘🐢🦁

## 🚀 실행 방법

**개발 환경:** Python 3.10 이상 (외부 라이브러리 없음, 표준 라이브러리 `json`, `pathlib`만 사용)

```bash
git clone https://github.com/SeungA-Ye/quiz-game.git
cd quiz-game
python3 main.py        # Windows는 python main.py
```

## 🎮 기능 목록

| 메뉴 | 기능 | 설명 |
|---|---|---|
| 1 | 퀴즈 풀기 | 등록된 문제를 순서대로 풀고 정답 여부와 최종 점수를 확인 |
| 2 | 퀴즈 추가 | 문제, 선택지 4개, 정답 번호를 입력해 새 퀴즈 등록 |
| 3 | 퀴즈 목록 | 등록된 모든 문제를 번호와 함께 확인 |
| 4 | 점수 확인 | 최고 점수 확인 (기록이 없으면 안내) |
| 0 | 종료 | 게임 종료 |
| - | 자동 저장/불러오기 | 퀴즈 추가·최고 점수 갱신 시 자동 저장, 실행 시 자동 불러오기 |

### 입력·예외 처리

| 상황 | 처리 |
|---|---|
| 앞뒤 공백 (` 1 `) | 공백 제거 후 처리 |
| 빈 입력 (Enter) | 안내 후 다시 입력 |
| 숫자가 아님 (`abc`) | 안내 후 다시 입력 |
| 범위 밖 숫자 (메뉴 `9`, 정답 `0`) | 안내 후 다시 입력 |
| `Ctrl+C` / 입력 종료(EOF) | 안내 메시지 출력 → 저장 → 안전 종료 |
| `state.json` 없음 | 기본 퀴즈 5개로 시작 |
| `state.json` 손상 | 안내 후 기본 퀴즈로 복구 |

## 📂 파일 구조

```
quiz-game/
├── main.py              # 실행 파일 (Quiz, QuizGame 클래스 및 게임 로직)
├── benchmark.py         # 퀴즈 개수별 저장·불러오기 성능 측정 스크립트
├── state.json           # 퀴즈 데이터 & 최고 점수 저장 파일 (실행 시 자동 생성, Git 추적 제외)
├── .gitignore           # Git 추적 제외 목록
├── README.md            # 프로젝트 설명 문서
└── docs/
    └── screenshots/     # 실행 화면 및 개발 환경 캡처
```

### 클래스 구조

| 클래스 | 역할 | 주요 메서드 |
|---|---|---|
| `Quiz` | 퀴즈 1개(문제·선택지·정답) | `show()` 출력, `is_correct()` 정답 확인, `to_dict()` / `from_dict()` 저장 형식 변환 |
| `QuizGame` | 게임 전체 관리 | `run()` 메뉴 반복, `play_quiz()`, `add_quiz()`, `show_list()`, `show_score()`, `save()`, `load()` |

### 클래스로 설계한 이유

**1. 추상화: 현실의 대상을 코드의 단위로 묶기**

퀴즈 1개는 항상 "문제 + 선택지 4개 + 정답"이 한 묶음으로 움직입니다. 클래스 없이 변수로 관리하면 `questions`, `choices`, `answers` 리스트 3개를 같은 순서로 맞춰야 하고, 하나만 어긋나도 엉뚱한 정답이 매칭됩니다. `Quiz` 클래스는 이 셋을 **하나의 객체**로 묶어, 퀴즈를 다룰 때 "퀴즈 1개"라는 단위로만 생각하게 해 줍니다.

**2. 재사용: 같은 틀로 여러 곳에서 퀴즈를 만들기**

`Quiz` 하나의 정의를 아래 세 곳에서 그대로 재사용합니다.

| 사용하는 곳 | 재사용 방식 |
|---|---|
| `get_default_quizzes()` | 기본 퀴즈 5개를 `Quiz(...)`로 생성 |
| `add_quiz()` | 사용자가 입력한 값으로 `Quiz(...)` 생성 |
| `load()` | 파일에서 읽은 딕셔너리를 `Quiz.from_dict()`로 복원 |

정답 확인 규칙(`is_correct`)이나 저장 형식(`to_dict`)을 바꿀 때 `Quiz` 클래스 **한 곳만** 고치면 세 곳에 모두 반영됩니다. 예를 들어 힌트 기능을 추가한다면 `Quiz`에 `hint` 속성 하나만 추가하면 됩니다.

**3. 책임 분리: 누가 무엇을 담당하는지 경계 나누기**

| 담당 | 책임 | 하지 않는 일 |
|---|---|---|
| `get_number()`, `get_text()` | **입력 수집·검증** (공백 제거, 빈 입력, 숫자 변환, 범위) | 게임 진행, 저장 |
| `Quiz` | **퀴즈 1개의 데이터와 규칙** (출력, 정답 확인, 저장 형식 변환) | 입력 받기, 파일 다루기 |
| `QuizGame` | **게임 흐름과 상태** (메뉴, 퀴즈 목록, 최고 점수, 파일 저장·불러오기) | 입력 검증 세부 규칙 |

이렇게 나누면 입력 규칙을 바꿀 때는 `get_number()`만, 저장 형식을 바꿀 때는 `Quiz.to_dict()` / `QuizGame.save()`만 고치면 되어 **변경 범위가 명확**해집니다.

## 💾 데이터 파일 설명 (state.json)

| 항목 | 내용 |
|---|---|
| 경로 | 프로젝트 루트 `quiz-game/state.json` (어느 위치에서 실행해도 `main.py`와 같은 폴더에 저장) |
| 역할 | 퀴즈 목록과 최고 점수를 저장해, 프로그램을 종료해도 데이터를 유지 |
| 인코딩 | UTF-8 (`ensure_ascii=False`로 한글을 그대로 저장) |
| 저장 시점 | 퀴즈 추가 시, 최고 점수 갱신 시, `Ctrl+C`로 종료 시 |

**스키마**

| 키 | 타입 | 설명 |
|---|---|---|
| `quizzes` | list | 퀴즈 객체 목록 |
| `quizzes[].question` | str | 문제 |
| `quizzes[].choices` | list[str] | 선택지 4개 |
| `quizzes[].answer` | int | 정답 번호 (1~4) |
| `best_score` | int | 최고 점수 (가장 많이 맞힌 문제 수) |

```json
{
  "quizzes": [
    {
      "question": "지구에 사는 동물 가운데 가장 큰 동물은?",
      "choices": ["대왕고래", "아프리카코끼리", "고래상어", "향유고래"],
      "answer": 1
    }
  ],
  "best_score": 4
}
```

## 🛟 state.json 백업 · 복구 절차

### 현재 프로그램의 자동 처리

| 상황 | 프로그램 동작 |
|---|---|
| 파일 없음 (첫 실행) | 기본 퀴즈 5개로 시작, 이후 저장 시 새로 생성 |
| 파일 손상 (JSON 문법 오류, 키 누락, 구조 오류) | 안내 후 기본 퀴즈로 복구 |
| 읽기 오류 (권한 등) | 안내 후 기본 퀴즈로 시작 |
| 쓰기 오류 | 안내 후 프로그램은 계속 실행 (해당 변경만 저장되지 않음) |

**한계:** 손상 시 기본 퀴즈로 복구되므로, 사용자가 **직접 추가한 퀴즈와 최고 점수는 사라집니다.** 이를 보완하기 위해 아래 백업 규칙을 사용합니다.

### 백업 규칙

- **언제:** 퀴즈를 여러 개 추가한 뒤, 또는 프로그램 구조를 수정하기 전
- **어디에:** 프로젝트 루트의 `state.backup.json` (`.gitignore`로 Git에는 올리지 않음)

```bash
cp state.json state.backup.json                                  # 백업
cp state.json "state.backup.$(date +%Y%m%d-%H%M).json"           # 날짜별 백업이 필요할 때
```

### 복구 절차

```bash
python3 -m json.tool state.backup.json > /dev/null && echo "백업 파일 정상"   # 1. 백업 파일이 올바른 JSON인지 확인
cp state.json state.broken.json                                              # 2. 손상된 파일은 원인 확인용으로 따로 보관
cp state.backup.json state.json                                              # 3. 백업으로 덮어쓰기
python3 main.py                                                              # 4. "📂 저장된 데이터를 불러왔습니다 (퀴즈 N개...)" 확인
```

### 권한 오류가 날 때

`파일을 읽을 수 없어...` 또는 `파일 저장 중 오류...`가 나오면 파일 권한을 확인합니다.

```bash
ls -l state.json          # 소유자에게 rw 권한이 있는지 확인 (예: -rw-r--r--)
chmod 644 state.json      # 소유자 읽기·쓰기 권한 부여
```

### 개선 계획

저장할 때 기존 파일을 `state.backup.json`으로 자동 복사하고, 손상이 감지되면 기본 퀴즈 대신 백업 파일에서 먼저 복구를 시도하는 방식으로 확장할 수 있습니다.

## 📈 대규모 데이터 성능 분석

퀴즈가 1,000개 이상으로 늘어났을 때도 동작하는지 `benchmark.py`로 측정했습니다. 실제 `state.json`은 건드리지 않고 임시 파일로만 측정합니다.

```bash
python3 benchmark.py
```

**측정 결과** (Python 3.14.4 · WSL2 Ubuntu 환경, 측정 시점마다 수치는 조금씩 달라질 수 있음)

| 퀴즈 수 | 파일 크기 | 저장 | 불러오기 | 목록 출력 | 불러오기 최대 메모리 |
|---:|---:|---:|---:|---:|---:|
| 5개 | 1.1 KB | 0.1 ms | 0.2 ms | 0.0 ms | 0.1 MB |
| 1,000개 | 213.8 KB | 13.2 ms | 8.0 ms | 0.2 ms | 1.0 MB |
| 10,000개 | 2,147.4 KB | 61.0 ms | 45.7 ms | 2.4 ms | 9.4 MB |
| 100,000개 | 21,571.2 KB | 442.6 ms | 476.5 ms | 18.4 ms | 93.7 MB |

**분석**

- 저장·불러오기 시간과 메모리는 퀴즈 수에 **거의 비례**해서 늘어납니다. 매번 **파일 전체**를 읽고 쓰는 방식이기 때문입니다.
- **10,000개까지는** 저장·불러오기가 0.1초 안팎으로 사용자가 지연을 느끼기 어렵습니다.
- **100,000개**에서는 불러오기 약 0.5초, 파일 약 21MB로, 퀴즈를 추가할 때마다 파일 전체를 다시 쓰는 비용이 커집니다.
- 실제 병목은 성능보다 **사용성**입니다. 퀴즈 풀기는 모든 문제를 순서대로 출제하므로, 1,000개면 1,000문제를 풀어야 끝납니다.

**개선 방안**

| 문제 | 방안 |
|---|---|
| 문제가 너무 많아 한 번에 다 풀 수 없음 | 출제 문제 수 선택 + `random.sample()`로 무작위 출제 |
| 파일이 커짐 | 저장 시 `indent=2` 제거로 파일 크기 축소 |
| 추가할 때마다 전체 파일 재작성 | 수십만 개 이상이면 표준 라이브러리 `sqlite3` 데이터베이스로 전환해 필요한 퀴즈만 읽고 쓰기 |

## 📸 실행 화면

### 🏠 메인 메뉴
![메인 메뉴](docs/screenshots/menu.png)

### 🎮 퀴즈 풀기
![퀴즈 풀기](docs/screenshots/play.png)

### ➕ 퀴즈 추가
![퀴즈 추가](docs/screenshots/add.png)

### 📋 퀴즈 목록
![퀴즈 목록](docs/screenshots/list.png)

### 🏆 점수 확인
![점수 확인](docs/screenshots/score.png)

### 🛠️ 개발 환경 (Python 버전 · Git 설정)
![개발 환경](docs/screenshots/version.png)

### 🌿 Git 커밋 그래프 (`git log --oneline --graph --all`)
![Git 로그](docs/screenshots/git-log-graph.png)

## 🖥️ 실행 로그 (터미널 출력)

아래는 WSL2 Ubuntu에서 `python3 main.py`를 실제로 실행한 터미널 출력입니다. (메뉴 반복 출력은 일부 생략)

<details open>
<summary><b>① 재실행 시 데이터 불러오기 + 퀴즈 풀기 (7문제 전부 정답, 최고 점수 갱신)</b></summary>

```
$ python3 main.py
📂 저장된 데이터를 불러왔습니다. (퀴즈 7개, 최고 점수 3)

==== 퀴즈 게임 ====
1. 퀴즈 풀기
2. 퀴즈 추가
3. 퀴즈 목록
4. 점수 확인
0. 종료
원하는 번호를 고르세요: 1
지구에 사는 동물 가운데 가장 큰 동물은?
1. 대왕고래
2. 아프리카코끼리
3. 고래상어
4. 향유고래
정답 번호를 입력하세요: 1
정답입니다! 🎉
땅 위에서 가장 빨리 달리는 동물은?
1. 사자
2. 캥거루
3. 얼룩말
4. 치타
정답 번호를 입력하세요: 4
정답입니다! 🎉
... (3~6번 문제 생략) ...
펭귄이 사는 곳은?
1. 남극
2. 사막
3. 정글
4. 초원
정답 번호를 입력하세요: 1
정답입니다! 🎉

최종 점수: 7 / 7
🏆 최고 점수를 갱신했어요!

원하는 번호를 고르세요: 0
게임을 종료합니다! 👋
```
</details>

<details open>
<summary><b>② 퀴즈 추가 (빈 문제·빈 선택지 입력 방지)</b></summary>

```
원하는 번호를 고르세요: 2

=== 퀴즈 추가 ===
문제를 입력하세요: 
입력이 비어있습니다. 다시 입력해주세요. 🙏
문제를 입력하세요: 펭귄이 사는 곳은?
1번 선택지: 
입력이 비어있습니다. 다시 입력해주세요. 🙏
1번 선택지: 남극
2번 선택지: 사막
3번 선택지: 정글
4번 선택지: 초원
정답 번호(1~4): 1
퀴즈가 추가되었어요! 🎉
```
</details>

<details open>
<summary><b>③ 퀴즈 목록 · 점수 확인</b></summary>

```
원하는 번호를 고르세요: 3

=== 퀴즈 목록 (총 7개) ===
[1] 지구에 사는 동물 가운데 가장 큰 동물은?
[2] 땅 위에서 가장 빨리 달리는 동물은?
[3] 땅 위에 사는 동물 가운데 키가 가장 큰 동물은?
[4] 꿀을 만드는 곤충은?
[5] 날개가 있지만 날지 못하는 새는?
[6] 다리가 가장 많은 동물은?
[7] 펭귄이 사는 곳은?

원하는 번호를 고르세요: 4

🏆 최고 점수: 3문제 정답
```
</details>

<details open>
<summary><b>④ 잘못된 입력 처리 (빈 입력 · 문자 · 범위 밖)</b></summary>

```
원하는 번호를 고르세요: 
입력이 비어있습니다. 다시 입력해주세요. 🙏
원하는 번호를 고르세요: abc
숫자만 입력해주세요! 🔢
원하는 번호를 고르세요: 9
0~4 사이로 입력해주세요! 😊

정답 번호를 입력하세요: abd
숫자만 입력해주세요! 🔢
```
</details>

<details open>
<summary><b>⑤ Ctrl+C(퀴즈 도중) · Ctrl+D(메뉴) 안전 종료</b></summary>

```
정답 번호를 입력하세요: ^C

입력이 중단되어 게임을 안전하게 종료합니다. 💾
$ python3 main.py

원하는 번호를 고르세요: 

입력이 중단되어 게임을 안전하게 종료합니다. 💾
```
</details>

<details open>
<summary><b>⑥ 퀴즈·기록이 없을 때 (빈 state.json으로 테스트)</b></summary>

```
$ cp state.json state.backup.json
$ echo '{"quizzes": [], "best_score": 0}' > state.json
$ python3 main.py
원하는 번호를 고르세요: 3
등록된 퀴즈가 없어요! 😢
원하는 번호를 고르세요: 4

아직 퀴즈를 푼 기록이 없어요! 먼저 퀴즈를 풀어보세요. 📝
원하는 번호를 고르세요: 1
풀 수 있는 퀴즈가 없어요! 😢
원하는 번호를 고르세요: 0
게임을 종료합니다! 👋
$ mv state.backup.json state.json
```
</details>

<details open>
<summary><b>⑦ 프로젝트 밖에서 실행해도 같은 state.json 사용</b></summary>

```
$ cd ~
$ python3 quiz-game/main.py
📂 저장된 데이터를 불러왔습니다. (퀴즈 7개, 최고 점수 3)
원하는 번호를 고르세요: 4

🏆 최고 점수: 3문제 정답
```
</details>

## 🌿 Git 작업 흐름

| 단계 | 사용 명령 | 내용 |
|---|---|---|
| 저장소 시작 | `git init`, `git add`, `git commit`, `git push` | `.gitignore`, `README.md` 작성 후 첫 커밋·푸시 |
| 기능 단위 커밋 | `git add`, `git commit` | 메뉴 → Quiz 클래스 → 퀴즈 풀기 → 목록 → 추가·점수 → 저장/불러오기 → README 순서로 커밋 |
| 브랜치 작업 | `git checkout -b fix/input-handling` | 입력·예외 처리 보완 6개 커밋을 별도 브랜치에서 진행 |
| 병합 | `git checkout main`, `git merge --no-ff fix/input-handling` | 병합 기록이 그래프에 남도록 `--no-ff` 사용 |
| 복제 실습 | `git clone ... quiz-game-clone` | 별도 폴더에 복제 후 README에 한 줄 추가 → commit → push |
| 가져오기 실습 | `git pull` | 원래 작업 폴더에서 pull로 변경사항 반영 확인 |

## 🔁 clone · pull 실습 로그 (터미널 출력)

<details open>
<summary><b>① 별도 폴더로 clone → README 한 줄 추가 → commit → push</b></summary>

```
$ cd ~
$ git clone https://github.com/SeungA-Ye/quiz-game.git quiz-game-clone
Cloning into 'quiz-game-clone'...
remote: Enumerating objects: 85, done.
remote: Counting objects: 100% (85/85), done.
remote: Compressing objects: 100% (52/52), done.
remote: Total 85 (delta 42), reused 70 (delta 27), pack-reused 0 (from 0)
Receiving objects: 100% (85/85), 189.71 KiB | 9.98 MiB/s, done.
Resolving deltas: 100% (42/42), done.
$ cd quiz-game-clone
$ ls -la
drwxr-xr-x  7 seunga seunga 4096 Nov 10 21:04 .git
-rw-r--r--  1 seunga seunga   39 Nov 10 21:04 .gitignore
-rw-r--r--  1 seunga seunga 1696 Nov 10 21:04 README.md
drwxr-xr-x  3 seunga seunga 4096 Nov 10 21:04 docs
-rw-r--r--  1 seunga seunga 8592 Nov 10 21:04 main.py
$ echo "" >> README.md
$ echo "> 이 줄은 복제한 저장소(quiz-game-clone)에서 추가했습니다. (clone·pull 실습)" >> README.md
$ git add README.md
$ git commit -m "Docs: clone 실습 - 복제 저장소에서 README 한 줄 추가"
[main 4776faa] Docs: clone 실습 - 복제 저장소에서 README 한 줄 추가
 1 file changed, 2 insertions(+)
$ git push origin main
To https://github.com/SeungA-Ye/quiz-game.git
   1a4a2a0..4776faa  main -> main
```
</details>

<details open>
<summary><b>② 원래 작업 폴더에서 pull → 반영 확인</b></summary>

```
$ cd ~/quiz-game
$ tail -2 README.md                       # pull 전
## 💭 프로젝트 소감
처음으로 Git과 클래스를 활용해 완성한 프로젝트라 뿌듯하다!
$ git pull
From https://github.com/SeungA-Ye/quiz-game
   1a4a2a0..4776faa  main       -> origin/main
Updating 1a4a2a0..4776faa
Fast-forward
 README.md | 2 ++
 1 file changed, 2 insertions(+)
$ tail -2 README.md                       # pull 후

> 이 줄은 복제한 저장소(quiz-game-clone)에서 추가했습니다. (clone·pull 실습)
```

pull 전에는 마지막 줄이 "프로젝트 소감"이었고, pull 후에는 복제 폴더에서 추가한 줄이 반영되었습니다. clone 폴더에 `state.json`이 없는 것은 `.gitignore`로 Git 추적에서 제외했기 때문입니다.
</details>

## ✍️ 커밋 메시지 규칙

**형식:** `타입: 변경 요약 (필요하면 괄호로 세부 내용)`

| 타입 | 언제 쓰나 | 이 저장소의 예 |
|---|---|---|
| `Feat` | 새 기능 추가 | `Feat: 퀴즈 추가,점수 확인 기능 구현` |
| `Fix` | 버그·잘못된 동작 수정 | `Fix: 퀴즈 풀기 정답 변수명 불일치(NameError) 수정 및 중복 변환 제거` |
| `Refactor` | 동작은 그대로, 코드 구조·이름 정리 | `Refactor: 변수명·주석 정리 및 숫자 변환을 try/except로 처리` |
| `Docs` | README 등 문서 수정 | `Docs: 프로젝트 소감 추가` |
| `Chore` | 설정·환경 파일 정리 | `Chore: 이미 추적 중이던 state.json을 추적 대상에서 제외` |
| `Merge` | 브랜치 병합 | `Merge: 입력·예외 처리 보완 브랜치 병합` |

**커밋 단위 규칙**

1. **기능 1개 = 커밋 1개**: 메뉴, Quiz 클래스, 퀴즈 풀기처럼 하나의 기능이 완성될 때마다 커밋합니다.
2. **실행 확인 후 커밋**: `python3 main.py`로 해당 기능을 끝까지 실행해 본 뒤 커밋합니다.
3. **관련 없는 변경은 나누기**: 기능 수정과 문서 수정은 서로 다른 커밋으로 분리합니다.

## 📊 커밋 기록

`git log --oneline | wc -l` 기준 **32개** 커밋 (아래 그래프는 28번째 커밋까지, 이후 성능 측정·문서 보완 커밋 4개 추가)

```
* f4b2cf3 Fix: 퀴즈 풀기 정답 변수명 불일치(NameError) 수정 및 중복 변환 제거
* 39fdc20 Docs: README 스키마·예외 처리·Git 작업 흐름 보완 및 실행 화면 갱신
* 4776faa Docs: clone 실습 - 복제 저장소에서 README 한 줄 추가
* 1a4a2a0 Fix: .gitignore에서 .vscode/와 state.json 규칙 분리
* 456fb13 Chore: 이미 추적 중이던 state.json을 추적 대상에서 제외
*   d12b3df Merge: 입력·예외 처리 보완 브랜치 병합
|\
| * fd9f584 Refactor: 변수명·주석 정리 및 숫자 변환을 try/except로 처리
| * 47c9f8e Fix: state.json 경로를 프로젝트 루트로 고정하고 저장·불러오기 오류 처리 보강
| * 0049b33 Fix: 빈 목록·기록 없는 점수 안내 및 목록 표시 개선
| * 68f3e84 Fix: 퀴즈 추가 시 빈 문제·선택지 입력 방지
| * 025bae3 Feat: Ctrl+C·EOF 발생 시 저장 후 안전 종료
| * 58fde27 Fix: 메뉴 입력에 공백,빈 입력,범위 검증 적용
|/
* 9ef66c3 Feat: 구축 환경, 로그 사진 추가
* 53b9e03 Docs: 프로젝트 소감 추가
* 1a3545c Feat: README.md 작성
* 949c296 Feat: state.json을 gitignore에 추가
* 04f495f Feat: 파일 저장/불러오기 기능 추가 및 손상 복구 처리
* 511322f Feat: 퀴즈 추가,점수 확인 기능 구현
* 984578c Feat: 퀴즈 플레이 기능 완성 (빈 퀴즈 처리, 최고점수 갱신)
* 30b65d4 Feat: 공통 입력 검증 함수 추가 (예외처리)
* b5bc854 Feat: 퀴즈 목록 보기 기능 구현
* aa88ed0 Feat: 퀴즈 풀기 기능 구현
* 495738f Feat: 게임 메뉴와 실행 반복 기능 구현
* e7ac430 Feat: 기본 퀴즈 데이터 2개 추가 (주제: 동물)
* bfdad96 Feat: 퀴즈 출력, 정답 입력, 정답 확인 기능 추가
* f41f5db Feat: Quiz 클래스 구현 (출력/정답확인)
* fde41a8 Feat: Quiz 클래스와 show 메서드 구현
* f885e34 Chore: 프로젝트 초기 설정 (gitignore, README)
```

**그래프 읽는 법:** `|\`에서 `fix/input-handling` 브랜치가 main에서 갈라지고, 6개 커밋 후 `|/`에서 `d12b3df Merge`로 main에 합쳐집니다.

## 💭 프로젝트 소감

처음으로 Git과 클래스를 활용해 완성한 프로젝트라 뿌듯하다!

> 이 줄은 복제한 저장소(quiz-game-clone)에서 추가했습니다. (clone·pull 실습)
