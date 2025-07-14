# 📅 Schedule_Maker

**Schedule_Maker** is a terminal-based Python application that helps you quickly create Google Calendar events. Designed
for speed and flexibility, it turns natural language inputs into structured calendar schedules.

---

## 🚀 Features

- ✅ Create individual events directly from your terminal
- 📆 Build recurring schedules with human-friendly syntax
- 🔌 Integrated with the Google Calendar API
- 🧩 Easily extendable and customizable for your own use case

---

## ⚙️ How It Works

Schedule_Maker understands input in a simple, natural format:

```
[Course Name] in [Location] from [Start Time] to [End Time] every [Day] by [Teacher]
```

You can also specify when the schedule should start by adding this simple line on top of the schedule block:

```
Schedule starts on [Date]
```

---

## 🛠️ Setup & Installation

✅ Requirements

- Python 3.8 or higher

- pip (Python package installer) or pipx

- (Optional but recommended) Python virtual environment

## 🔧 Installation Steps

1. Clone the repository
2. Add your Google API credentials
    - Place the provided credentials.json file into the secrets/ directory.
    - If you don’t have the credentials, contact the project maintainer.

3. Activate the virtual environment if it's not already

4. Go to the project root and install the project using
   ```
   pip install --editable .
   ```
   If you want the sm command to be available outside the .venv use
   ```
   pipx install --editable .
   ```

---

## 📬 Contact

For credentials or other inquiries, feel free to reach out to me.

---
Feel free to give me advices on how to make the code better. I am here to learn.