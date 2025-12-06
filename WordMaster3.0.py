import json
import os
import random
from datetime import datetime, timedelta

# =================== SETTINGS ===================
ENG_FILE = "eng.txt"
RUS_FILE = "rus.txt"
DATA_FILE = "wm3_data.json"

SESSION_SIZE = 10
MAX_SCORE = 4

# =================== UTILITIES ===================
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def load_words():
    with open(ENG_FILE, encoding="utf-8") as f:
        eng = [x.strip() for x in f if x.strip()]
    with open(RUS_FILE, encoding="utf-8") as f:
        rus = [x.strip() for x in f if x.strip()]
    if len(eng) != len(rus):
        print("eng.txt and rus.txt must have the same number of lines!")
        exit()
    return eng, rus

# =================== INITIALIZATION ===================
def init_data():
    eng, rus = load_words()
    today = str(datetime.now().date())
    data = {}

    for e, r in zip(eng, rus):
        data[e] = {
            "rus": r,
            "score": 0,
            "interval": 1,
            "next_review": today,
            "mistakes": 0,
            "hard": False,
            "learned": False
        }

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return data

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return init_data()

# =================== SELECT SESSION WORDS ===================
def select_words(data):
    today = datetime.now().date()

    due = [
        w for w in data
        if datetime.fromisoformat(data[w]["next_review"]).date() <= today
        and not data[w]["learned"]
    ]

    hard = [w for w in due if data[w]["hard"]]
    normal = [w for w in due if not data[w]["hard"]]

    random.shuffle(hard)
    random.shuffle(normal)

    # prioritize some hard words, then fill with normal ones
    session = hard[:5] + normal
    return session[:SESSION_SIZE]

# =================== UPDATE WORD AFTER ANSWER ===================
def update_word(w, data, correct):
    today = datetime.now().date()

    if correct:
        data[w]["score"] += 1
        data[w]["mistakes"] = 0
        data[w]["hard"] = False
        data[w]["interval"] += 1
    else:
        data[w]["score"] = max(0, data[w]["score"] - 1)
        data[w]["mistakes"] += 1
        data[w]["hard"] = True
        data[w]["interval"] = 1

    data[w]["next_review"] = str(today + timedelta(days=data[w]["interval"]))

    if data[w]["score"] >= MAX_SCORE:
        data[w]["learned"] = True
        print(f"Word '{w}' is fully learned and removed!")

# =================== SHOW STATISTICS ===================
def show_stats(data):
    total = len(data)
    learned = len([w for w in data if data[w]["learned"]])
    hard = len([w for w in data if data[w]["hard"]])

    print("STATISTICS")
    print(f"Total words: {total}")
    print(f"Learned: {learned}")
    print(f"Hard words: {hard}")

# =================== MAIN ===================
def main():
    data = load_data()
    session = select_words(data)

    if not session:
        print("No words to review today. Come back tomorrow!")
        input("\nPress Enter to exit...")
        return

    show_stats(data)
    input("\nPress Enter to start the session...")

    for word in session:
        clear()
        rus = data[word]["rus"]
        answer = input(f"Translate: {rus} → ").strip().lower()

        if answer == word.lower():
            print("Correct!")
            correct = True
        else:
            print(f"Wrong! Correct answer: {word}")
            correct = False

        update_word(word, data, correct)
        input("\nPress Enter to continue...")

    # save progress
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    clear()
    show_stats(data)
    print("\nSession finished!")
    input("\nPress Enter to exit...")  # final pause so console doesn't close immediately

if __name__ == "__main__":
    main()
