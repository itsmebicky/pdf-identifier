# PDF IDENTIFIER Tool with OCR AND Tkinter

This Python application allows you to open a PDF file, select areas for Optical Character Recognition (OCR), and save the extracted text along with the selected coordinates into either a CSV file or a JSON file. It utilizes Tkinter for the graphical interface, PyMuPDF for PDF handling, and Tesseract for OCR.

## Features

- **PDF Viewing**: Display the first page of a PDF file with zoom and scroll capabilities.
- **OCR Selection**: Select areas on the PDF page to perform OCR.
- **Data Saving**: Save OCR results and selected coordinates into CSV or JSON formats.
- **Multiple Operations**: Choose between two operations: single area OCR and structured data extraction.

## Requirements

- Python 3.x
- `tkinter` (usually included in Python standard library)
- `PyMuPDF` (`fitz` module)
- `Pillow` (PIL fork for image handling)
- `pytesseract` (Tesseract OCR Python wrapper)

## Installation

1. **Clone the repository**:
   git clone https://github.com/itsmebicky/pdf-identifier.git

2. **Install dependencies**:
   Make sure you have Tesseract installed on your system. You can install it from [here](https://github.com/tesseract-ocr/tesseract).

## Usage

1. **Run the application**:
   python main.py


2. **Select operation type**:
- Enter `1` to perform single area OCR and save results to CSV.
- Enter `2` to extract structured data and save results to JSON.

3. **PDF Selection**:
- Update `pdf_path` variable in `main.py` to point to your PDF file.

4. **Perform OCR**:
- For single area OCR (`operation_type == '1'`):
  - Select an area on the PDF page using mouse drag.
  - Enter a format type (e.g., "section1") when prompted.
  - OCR text will be extracted, and results will be saved to a CSV file.

- For structured data extraction (`operation_type == '2'`):
  - Define key-value pairs by selecting regions alternately.
  - Enter names for keys and values when prompted.
  - Data will be structured and saved to a JSON file.

5. **Exit the application**:
- Close the window or press `Ctrl + C` in the terminal to save the final JSON file.

## Contributing

Contributions are welcome! Here are a few guidelines:

- Fork the repository and clone it locally.
- Create a new branch for your feature or bug fix.
- Commit your changes and push to your fork.
- Submit a pull request with a detailed description of your changes.


## Acknowledgments

- This project utilizes libraries like Tkinter, PyMuPDF, Pillow, and pytesseract.
- Inspired by the need for a simple yet effective PDF OCR tool with GUI capabilities.

   
