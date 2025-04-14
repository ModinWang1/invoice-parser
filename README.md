# 🧾 Invoice Parser

This project is a visual invoice parser powered by [DeepSeek-VL2-tiny](https://huggingface.co/deepseek-ai/DeepSeek-VL2), a multimodal vision-language model. It extracts structured data from invoice or receipt images and outputs a clean `.csv` file containing relevant information like vendor, invoice number, date, line items, and totals.

---

## ✨ Features

- Accepts invoice images (`.jpg`, `.png`, etc.)
- Automatically extracts:
  - Vendor name
  - Invoice number
  - Invoice date
  - Purchase order or job number
  - Itemized descriptions, quantities, and prices
  - Subtotal, tax, and total
- Exports structured `.csv` output
- Offers both a **Streamlit UI** and **script-based batch processing**

---

## 🚀 How to Run This Project

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/invoice-parser.git
cd invoice-parser
```

---

### 2. Create a virtual environment (optional but recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ **Note**: You'll also need to have **PyTorch** installed with CUDA if you want GPU acceleration. You can get the correct install command from: https://pytorch.org/get-started/locally/

---

### 4. Download the DeepSeek-VL2-tiny model

You can either:

#### A. Pull the model automatically via Hugging Face (preferred):

Ensure `main.py` or your model loader uses:
```python
model = AutoModelForVision2Seq.from_pretrained("deepseek-ai/DeepSeek-VL2", trust_remote_code=True)
```

#### B. Or place the downloaded model files in the `models/` directory if working offline.

---

## 🧪 Option 1: Try It With Streamlit (Visual Demo)

```bash
streamlit run app.py
```

Then open your browser to the link shown in the terminal, usually:  
[http://localhost:8501](http://localhost:8501)

### What to do:
- Upload invoice images via the UI
- See extracted data live
- Download results as a `.csv`

---

## ⚙️ Option 2: Run From Command Line (Batch Mode)

### 1. Place your invoice images in the folder `invoices_as_images/`

```bash
invoices_as_images/
├── invoice1.jpg
├── invoice2.png
└── ...
```

### 2. Run the processing script:

```bash
python main.py
```

### 3. Output will be saved to:

```bash
output.csv
```

---

## 🖥️ Minimum System Requirements

- Python 3.9+
- 8–16 GB VRAM	16–32 GB RAM
- Optional: NVIDIA GPU with CUDA support for faster inference
- Disk space: Model files are several hundred MB in size

---

## 📦 Files to Know

| File | Purpose |
|------|---------|
| `app.py` | Streamlit frontend |
| `main.py` | Backend script for bulk image processing |
| `csv_writer.py` | Helper for writing extracted data to CSV |
| `reader.py` | Model logic for parsing invoice images |
| `parse_output.py` | Extract structured info from model output |

---

## 🤝 Contributions

Feel free to fork the repo, open issues, or suggest enhancements via pull requests!

---

## 📜 License

MIT License.

---

by Modin Wang