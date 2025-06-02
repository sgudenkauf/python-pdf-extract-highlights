# ✨ PDF Highlight Extractor

**Do you highlight PDF texts in Microsoft Edge, GoodReader, or Adobe Acrobat?**  
This tool helps you **extract all those highlights automatically** – color-coded, neatly sorted, and saved to a clean Markdown file.

![Example highlight in a pdf document](/img/pdf-highlight-example.png)  
*Fig. 1: Example highlight in a pdf document.*

## 🔍 What It Does

This Python script scans your PDF for highlight annotations and exports them into a structured Markdown file:

- Grouped by color (e.g. Yellow, Red, Green, etc.)
- Sorted by page number
- Output in clean, readable `.md` format

> **Sample Output:**
>
> ```md
> ## Yellow
>
> ### Page 1
> This is a yellow-highlighted sentence.
>
> ### Page 3
> Another one in yellow.
> ```

## ✅ Works With Highlights From

- 🖥️ Microsoft Edge (desktop)
- 📱 GoodReader (iPad)
- 📄 Adobe Acrobat
- …and most PDF apps that support proper annotations

## 🚀 How to Use

### 1. Install the required library

Make sure [`PyMuPDF`](https://pymupdf.readthedocs.io/) is installed:

```bash
pip install pymupdf
```

### 2. Make it executable (optional, Linux/macOS)

```bash
chmod +x extract_highlights.py
```

### 3. Run it

```bash
./extract_highlights.py yourfile.pdf highlights.md
```

Or using Python directly:

```bash
python extract_highlights.py yourfile.pdf highlights.md
```

## 🎨 Color Recognition

The tool recognizes highlights in: Yellow, Red, Green, Blue, Cyan, Magenta, Orange, Gray.  
Unrecognized tints will be grouped under “Unknown.” A color tolerance ensures reliable results even with subtle differences.

## ⚠️ Limitations

- It won't extract highlights from “flattened” or scanned PDFs (annotations must still exist).
- Text in images or OCR layers is not supported.

## 🧠 How It Works

It analyzes the geometric coordinates of highlight annotations to extract only the text **that truly overlaps the highlighted area** (≥50% area overlap). This ensures accurate results – no extra lines or unmarked text.

## 📝 License (MIT)

Copyright (c) 2025 Stefan Gudenkauf

**MIT License** – free to use, modify, and share. No warranty.

---

✨ Whether you’re a student, researcher, or lifelong note-taker – this tool keeps your highlights tidy and your mind focused.