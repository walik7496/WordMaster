import json
import random
import os

# -------------------- SETTINGS --------------------
ENG_FILE = "eng.txt"
RUS_FILE = "rus.txt"
SAVE_FILE = "words_to_learn.json"
HARD_FILE = "hard_words.txt"

SESSION_WORDS = 10     # 🔥 how many words per session AND in JSON
MAX_SCORE = 5
HARD_THRESHOLD = 3

# -------------------- LOAD MAIN DICTIONARIES --------------------
with open(ENG_FILE, encoding="utf-8") as f:
    eng_words = [line.strip() for line in f.readlines()]

with open(RUS_FILE, encoding="utf-8") as f:
    rus_words = [line.strip() for line in f.readlines()]

if len(eng_words) != len(rus_words):
    print("eng.txt and rus.txt must have the same number of lines!")
    exit()

all_words = dict(zip(eng_words, rus_words))

# -------------------- LOAD HARD WORDS --------------------
hard_words = set()
if os.path.exists(HARD_FILE):
    with open(HARD_FILE, encoding="utf-8") as f:
        for line in f:
            hard_words.add(line.strip())

# -------------------- LOAD OR CREATE SESSION --------------------
def load_next_session():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            session = json.load(f)
    else:
        session = {}

    if not session:
        remaining = list(all_words.items())
        if not remaining:
            return None

        next_batch = remaining[:SESSION_WORDS]
        session = {
            eng: {"rus": rus, "score": 0, "mistakes": 0}
            for eng, rus in next_batch
        }

        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(session, f, ensure_ascii=False, indent=4)

    return session

words_data = load_next_session()

if not words_data:
    print("All words have been learned!")
    exit()

# -------------------- SMART WORD PICK --------------------
def choose_word():
    weighted = []
    for eng, data in words_data.items():
        weight = max(1, 6 - data["score"])
        if eng in hard_words:
            weight += 3
        weighted.extend([eng] * weight)
    return random.choice(weighted)

# -------------------- MAIN LEARNING LOOP --------------------
questions_today = 0

while words_data and questions_today < SESSION_WORDS:
    eng = choose_word()
    rus = words_data[eng]["rus"]

    hint = ""
    if words_data[eng]["mistakes"] >= 3:
        hint = f" (hint: {eng[0]})"

    answer = input(f"Translate '{rus}' into English{hint}: ").strip().lower()

    if answer == eng.lower():
        print("Correct!")
        words_data[eng]["score"] += 1
        words_data[eng]["mistakes"] = 0

        if words_data[eng]["score"] >= MAX_SCORE:
            print(f"Word '{eng}' is fully learned and removed!")
            del words_data[eng]

            if eng in hard_words:
                hard_words.remove(eng)

            if eng in eng_words:
                idx = eng_words.index(eng)
                eng_words.pop(idx)
                rus_words.pop(idx)

                with open(ENG_FILE, "w", encoding="utf-8") as f:
                    f.write("\n".join(eng_words))

                with open(RUS_FILE, "w", encoding="utf-8") as f:
                    f.write("\n".join(rus_words))

    else:
        print(f"Wrong. Correct: {eng}")
        words_data[eng]["score"] = max(0, words_data[eng]["score"] - 1)
        words_data[eng]["mistakes"] += 1
        if words_data[eng]["mistakes"] >= HARD_THRESHOLD:
            hard_words.add(eng)

    questions_today += 1

    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(words_data, f, ensure_ascii=False, indent=4)

    with open(HARD_FILE, "w", encoding="utf-8") as f:
        for w in hard_words:
            f.write(w + "\n")

# -------------------- NEXT SESSION AUTO-LOAD --------------------
if not words_data:
    print("\nSession completed! Loading new words next time.")

print(f"\nSession finished. Questions today: {questions_today}")
