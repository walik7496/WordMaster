import json
import os
import random
from datetime import datetime, timedelta

# ---------------- SETTINGS ----------------
ENG_FILE = "eng.txt"
RUS_FILE = "rus.txt"
DATA_FILE = "words_data.json"

SESSION_NEW = 15
SESSION_TOTAL = 50
HARD_WEIGHT = 2
TOP_HARD = 10

# ---------------- COLORS ----------------
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# ---------------- UTILS ----------------
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def load_words():
    with open(ENG_FILE, encoding="utf-8") as f:
        eng = [x.strip() for x in f if x.strip()]
    with open(RUS_FILE, encoding="utf-8") as f:
        rus = [x.strip() for x in f if x.strip()]
    if len(eng) != len(rus):
        raise ValueError("eng.txt and rus.txt must have the same number of lines!")
    return eng, rus

def initialize_data(eng_list, rus_list):
    data = {}
    today = str(datetime.now().date())
    for e, r in zip(eng_list, rus_list):
        data[e] = {
            "rus": r,
            "ease": 2.5,
            "interval": 1,
            "repetitions": 0,
            "next_review": today,
            "hard": False,
            "mistakes": 0
        }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return data

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        eng, rus = load_words()
        return initialize_data(eng, rus)

# ---------------- SELECT WORDS ----------------
def select_words(data):
    today = datetime.now().date()
    due = [w for w in data if datetime.fromisoformat(data[w]["next_review"]).date() <= today]
    random.shuffle(due)
    
    new_words = [w for w in due if data[w]["repetitions"] == 0][:SESSION_NEW]
    repeat_words = [w for w in due if w not in new_words]
    
    weighted_list = []
    for w in repeat_words:
        weight = HARD_WEIGHT if data[w]["hard"] else 1
        weighted_list.extend([w]*weight)
    
    session_words = new_words + weighted_list
    random.shuffle(session_words)
    return session_words[:SESSION_TOTAL]

# ---------------- SPACED REPETITION ----------------
def update_word(w_data, correct):
    today = datetime.now().date()
    if correct:
        quality = 3
    else:
        quality = 0

    if quality < 2:
        w_data["repetitions"] = 0
        w_data["interval"] = 1
        w_data["hard"] = True
        w_data["mistakes"] += 1
    else:
        w_data["repetitions"] += 1
        w_data["interval"] = max(1, int(w_data["interval"] * w_data["ease"]))
        w_data["ease"] += 0.1
        w_data["hard"] = False
        w_data["mistakes"] = 0

    w_data["next_review"] = str(today + timedelta(days=w_data["interval"]))

# ---------------- PROGRESS ----------------
def show_progress(data):
    total_words = len(data)
    mastered = len([w for w in data if data[w]["repetitions"] > 0 and not data[w]["hard"]])
    hard = len([w for w in data if data[w]["hard"]])
    due_today = len([w for w in data if datetime.fromisoformat(data[w]["next_review"]).date() <= datetime.now().date()])

    print(f"\n📊 Progress:")
    print(f"Total words: {total_words}")
    print(f"Mastered: {mastered} ({mastered/total_words*100:.1f}%)")
    print(f"Hard words: {hard} ({hard/total_words*100:.1f}%)")
    print(f"Words due today: {due_today}\n")

def show_top_hard(data):
    hard_words = sorted([w for w in data if data[w]["hard"]], key=lambda x: data[x]["mistakes"], reverse=True)
    print(f"{YELLOW}🔥 Top {TOP_HARD} hard words:{RESET}")
    for w in hard_words[:TOP_HARD]:
        print(f"{data[w]['rus']} → {w} | mistakes: {data[w]['mistakes']}")
    print()

# ---------------- MAIN LOOP ----------------
def main():
    data = load_data()
    session_words = select_words(data)

    if not session_words:
        print("No words for today. Come back tomorrow ✅")
        return

    show_progress(data)

    for eng in session_words:
        clear()
        rus = data[eng]["rus"]
        answer = input(f"Translate '{rus}' → ").strip().lower()

        if answer == eng.lower():
            print(f"{GREEN}✅ Correct!{RESET}")
            correct = True
        else:
            print(f"{RED}❌ Wrong!{RESET} | Correct: {eng}")
            correct = False

        update_word(data[eng], correct)
        input("\nPress Enter to continue...")

    # save progress
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    show_progress(data)
    show_top_hard(data)
    print("\n✅ Session finished.")

# ---------------- RUN ----------------
if __name__ == "__main__":
    main()
