# 🌟 WordMaster

**WordMaster** is a smart console program for learning English words from Russian using adaptive repetition and small learning sessions.

The program is designed to keep you motivated by loading only a small number of words per session and automatically removing learned words from your dictionaries.

---

## 🚀 Features

- 🧠 **Smart repetition system** — words you struggle with appear more often  
- 📦 **Session-based learning** — only a limited number of words per session (default: 10)  
- ✅ **Automatic word removal** — fully learned words are removed from:
  - `words_to_learn.json`
  - `eng.txt`
  - `rus.txt`
- 🔥 **Hard words tracking** — difficult words are saved in `hard_words.txt`  
- 💡 **Hints** — after several mistakes, the first letter is shown  
- 💾 **Progress saving** — you can safely close the program and continue later  

---

## 📂 Project Files

| File | Description |
|------|-------------|
| `eng.txt` | English words (one per line) |
| `rus.txt` | Russian translations (same order as `eng.txt`) |
| `words_to_learn.json` | Current learning session (max `SESSION_WORDS` words) |
| `hard_words.txt` | Frequently mistaken words |
| `wordmaster.py` | Main program file |

---

## ⚙️ Settings

Edit these values directly in `wordmaster.py`:

```python
SESSION_WORDS = 10    # number of words per session AND in JSON
MAX_SCORE = 5         # score required to fully learn a word
HARD_THRESHOLD = 3   # mistakes before a word becomes "hard"
▶️ How to Run

Install Python 3

Put these files in one folder:

wordmaster.py

eng.txt

rus.txt

Run the program:

python wordmaster.py


Translate the Russian word into English.

After a word reaches MAX_SCORE, it is permanently removed.

When all session words are learned, new words will be loaded automatically next time.

⚠️ Important (First Launch)

Before the first run or after changing SESSION_WORDS:

✅ Delete:

words_to_learn.json


This allows the program to generate a fresh session with the correct number of words.

📈 Future Ideas

📊 Daily learning statistics

🔁 Quick review mode

🔊 Word pronunciation

↔ Bidirectional learning (EN → RU & RU → EN)

📱 Mobile or web version

📝 License

MIT License © 2025
