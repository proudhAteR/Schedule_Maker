# Schedule_Maker

Schedule_Maker is a Python-based application that helps extract and organize course or event schedules from PDF or image
files using OCR (Optical Character Recognition). The tool processes timetable documents and converts them into
structured, human-readable descriptions.

## 📌 Features

- Supports extraction from scanned PDFs and images.
- Uses OCR to identify and parse tabular schedule content.

## ⚙️ How It Works

1. The user provides a PDF or image file containing a class or event schedule.
2. The app uses OCR (like PaddleOCR or Tesseract) to detect text within the file.
3. A parser extracts schedule information based on positional and confidence data.

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

- `paddleocr`
- `pytesseract`
- `pdf2image`
- `Pillow`
- `opencv-python`
- `numpy`
- `google-api-core`

### Additional Requirements (System Dependencies)

You must install [Poppler](https://poppler.freedesktop.org/) for `pdf2image` to work:

- On macOS:

```bash
  brew install poppler
```

**Note:** You may also need to install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) engine or [Paddle OCR](https://github.com/PaddlePaddle/PaddleOCR) system dependencies based on your OS.

- On macOs:

```bash
  brew install tesseract
```

## ⚠️ Limitations

- OCR accuracy depends on the quality and structure of the input document.
- Tables with irregular formatting, merged cells, or handwritten notes may not be parsed correctly.
- Current version assumes a standard weekly schedule format; custom or non-standard layouts may require additional
  processing logic.

---

Feel free to contribute by submitting pull requests or reporting issues!
