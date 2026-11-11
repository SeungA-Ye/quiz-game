"""퀴즈 개수에 따른 저장·불러오기·목록 성능 측정 스크립트.

실제 게임 데이터(state.json)는 건드리지 않고, 임시 폴더의 파일로만 측정한다.
실행: python3 benchmark.py
"""
import contextlib
import io
import tempfile
import time
import tracemalloc
from pathlib import Path

import main
from main import Quiz, QuizGame

SIZES = [5, 1_000, 10_000, 100_000]


def make_game(count):
    """count개의 퀴즈를 가진 QuizGame을 load() 없이 만든다."""
    game = QuizGame.__new__(QuizGame)
    game.quizzes = [
        Quiz(f"문제 {i}: 지구에서 가장 큰 동물은?",
             ["대왕고래", "아프리카코끼리", "기린", "타조"], 1)
        for i in range(count)
    ]
    game.best_score = 3
    return game


def measure(count):
    game = make_game(count)

    start = time.perf_counter()
    game.save()
    save_ms = (time.perf_counter() - start) * 1000
    size_kb = main.STATE_FILE.stat().st_size / 1024

    loaded = QuizGame.__new__(QuizGame)
    tracemalloc.start()
    start = time.perf_counter()
    with contextlib.redirect_stdout(io.StringIO()):
        loaded.load()
    load_ms = (time.perf_counter() - start) * 1000
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    start = time.perf_counter()
    with contextlib.redirect_stdout(io.StringIO()):
        loaded.show_list()
    list_ms = (time.perf_counter() - start) * 1000

    return size_kb, save_ms, load_ms, list_ms, peak / 1024 / 1024


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        main.STATE_FILE = Path(tmp) / "state.json"     # 실제 state.json 보호
        print("| 퀴즈 수 | 파일 크기 | 저장 | 불러오기 | 목록 출력 | 불러오기 최대 메모리 |")
        print("|---:|---:|---:|---:|---:|---:|")
        for n in SIZES:
            size_kb, save_ms, load_ms, list_ms, peak_mb = measure(n)
            print(f"| {n:,}개 | {size_kb:,.1f} KB | {save_ms:,.1f} ms | "
                  f"{load_ms:,.1f} ms | {list_ms:,.1f} ms | {peak_mb:,.1f} MB |")
