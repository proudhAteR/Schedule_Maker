# 📅 Schedule_Maker

**Schedule_Maker** is a terminal-based Python application that helps you quickly create Google Calendar events. Designed
for speed and flexibility, it turns natural language inputs into structured calendar schedules.


---

## 🚀 Features

- ✅ Create events directly from your terminal
- 📆 Build recurring schedules with human-friendly syntax
- 🔌 Integrates with the Google Calendar API
- 🧩 Easily extendable and customizable

---

## ⚙️ How It Works

Schedule_Maker understands input in a simple, natural format:

```
[Course Name] in [Location] from [Start Time] to [End Time] every [Day] by [Teacher]
```

Example:

```
Math in Room A from 10:00 to 11:00 every Monday by John
```

For more information on the commands use:

   ```bash
     sm --help
   ```

---

## 🛠️ Setup & Installation

✅ Requirements

- Python 3.10+

- pip (Python package installer)
  or [pipx](https://chatgpt.com/c/6877e1e7-0dc4-8009-8399-99b5171f3aa1#:~:text=pip%20or-,pipx,-(Recommended)%20Python%20virtual)

- (Optional but recommended) Python virtual environment

## 🔧 Installation Steps

1. Clone the repository
   ```bash
   git clone https://github.com/proudhAteR/Schedule_Maker.git
   cd Schedule_Maker
   ```

2. Add your Google API credentials
    - Place your credentials.json file into the secrets/ directory.
    - If you don’t have it, contact the project maintainer (see contact info below).

3. Activate the virtual environment if it's not already (Optional)

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   ````

4. Go to the project root and install the project using

   ```bash
   pip install -e .
   ````
   If you don't want to use a virtual environment use:
   ```bash
   pipx install -e .
   ````
---

## 📬 Contact

Need help with credentials or want to contribute?

📧 Email: cboleku162004@gmail.com

💬 GitHub: @proudhAteR

---

## 🙏 Feedback & Contributions

I'm always looking to improve!
Feel free to suggest code improvements, open issues, or submit pull requests.
This project is both a tool and a learning journey.