# 📅 Schedule_Maker

**Schedule_Maker** is a terminal-based Python application that helps you quickly create Google Calendar events. Designed
for speed and flexibility, it turns natural language inputs into structured calendar schedules.

---

## 🆕 Changelog

### v0.1.7 (2025‑07‑22)

#### ✨ Added

- **Overview Command**: You can now get a quick summary of your schedule for a specific date.
    - Running the command **without** the `-o` / `--on` option shows the schedule for **today** by default:
      ```bash
      sm overview
      ```
    - Using the `-o` / `--on` option lets you choose a specific date:
      ```bash
      sm overview -o tomorrow
      ```
- Improved Natural Language Processing: Thanks to [`spaCy`](https://spacy.io/), the app's NLP capabilities are now more
  accurate and flexible.

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
Math in Room A from 8am to 1pm every Monday by John
```

### 🗣️ Input Examples

- `BIO200 Lab in Science Wing from 08:15 to 10:45 every Friday by Dr. Li`
- `Piano lesson in music room from 16 to 17 every Sunday by Mr. Bennett`
- `Cours de mathématiques dans la salle B de 9h à 11h chaque lundi par M. Dupont` *(French)*
- `Trabajo en oficina en la tarde todos los martes` *(Spanish)*

---

For more information on the commands use:

   ```bash
     sm --help
   ```

## 🛠️ Setup & Installation

✅ Requirements

- ![Python version](https://img.shields.io/badge/python-3.10%2B-blue)

- pip (Python package installer)
  or [pipx](https://pypa.github.io/pipx/)

- (Optional but recommended) Python virtual environment

### 🔧 Installation Steps

1. If you want the app to be installed in your venv:
   ```bash 
   pip install git+https://github.com/proudhAteR/Schedule_Maker.git
    ```
2. If you want the installation to be global run:
   ```bash 
   pipx install git+https://github.com/proudhAteR/Schedule_Maker.git
    ```

### 🔄 Upgrade Instructions
- If installed via pipx (recommended for global use):
    ```bash
    pipx upgrade sm
    ```
- If installed manually in a virtual environment:
  1. Activate your virtual environment:
      ```bash
     source .venv/bin/activate  # or .venv\Scripts\activate on Windows
      ```
  2. Run the upgrade command:
     ```bash
      pip install --upgrade git+https://github.com/proudhAteR/Schedule_Maker.git
       ```
---

## 📬 Contact

Need help with anything or want to contribute?

📧 Email: cboleku162004@gmail.com

💬 GitHub: @proudhAteR

---

## 🙏 Feedback & Contributions

I'm always looking to improve!
Feel free to suggest code improvements, open issues, or submit pull requests.
This project is both a tool and a learning journey.

---

## 📚 Table of Contents

- [What's New](#-changelog)
- [Features](#-features)
- [How It Works](#-how-it-works)
- [Setup & Installation](#-setup--installation)
- [Contact](#-contact)
