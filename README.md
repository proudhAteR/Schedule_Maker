# Schedule_Maker

Schedule_Maker is a Python-based application that helps create events using google calendar from the terminal. These
events are defined as classes but the code can easily be changed to fit the user needs.

## 📌 Features

- Create single events rapidly using the CLI
- Create schedules

## ⚙️ How It Works

1. The user enter a phrase like [Course Name] in [Location] from [Start Time] to [End Time] every [Day] by [Teacher]
   Example: Math in Room 101 from 10:00 to 11:00 every Monday by Mr. Smith
2. The event is created using the Google Calendar API (do not forget to contact me for the credentials.)

## 🧰 Prerequisites

- Python 3.8+
- pip
- Virtual environment recommended
- Add the given credentials.json file into the secrets directory

### Required Python packages:

Install all dependencies using:

```bash
  pip install -r requirements.txt
```

Dependencies typically include:

- `google-api-core`

---

Feel free to contribute by submitting pull requests or reporting issues!
