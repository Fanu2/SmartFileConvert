import streamlit as st
import pandas as pd
import pdfplumber
from PIL import Image
from fpdf import FPDF
from docx import Document
import json
import os

# --- Conversion Functions ---

def csv_to_excel(file):
    df = pd.read_csv(file)
    output_path = "output.xlsx"
    df.to_excel(output_path, index=False)
    return output_path

def excel_to_csv(file):
    df = pd.read_excel(file)
    output_path = "output.csv"
    df.to_csv(output_path, index=False)
    return output_path

def json_to_csv(file):
    output_path = "output.csv"
    try:
        data = json.load(file)
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            df = pd.json_normalize(data)
        else:
            raise ValueError("Unsupported JSON format")
        df.to_csv(output_path, index=False)
        return output_path
    except Exception:
        return None

def pdf_to_text(file):
    output_path = "output.txt"
    with pdfplumber.open(file) as pdf, open(output_path, "w", encoding="utf-8") as out:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                out.write(text + "\n")
    return output_path

def images_to_pdf(files):
    pdf = FPDF()
    pdf.set_auto_page_break(0)
    temp_files = []

    for file in files:
        img = Image.open(file)
        temp_path = f"temp_{file.name}"
        img = img.convert("RGB")
        img.save(temp_path)
        temp_files.append(temp_path)

        pdf.add_page()
        pdf.image(temp_path, x=10, y=10, w=190)

    output_path = "output.pdf"
    pdf.output(output_path)

    # Clean up temp files
    for temp_file in temp_files:
        try: os.remove(temp_file)
        except: pass

    return output_path

def txt_to_docx(file):
    output_path = "output.docx"
    text = file.read().decode("utf-8")
    doc = Document()
    doc.add_paragraph(text)
    doc.save(output_path)
    return output_path

def txt_to_html(file):
    output_path = "output.html"
    text = file.read().decode("utf-8")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("<html><body><pre>{}</pre></body></html>".format(text))
    return output_path

# --- Streamlit App ---

def main():
    st.title("Master File Converter App")

    conversion_type = st.selectbox(
        "Select Conversion Type",
        [
            "CSV to Excel",
            "Excel to CSV",
            "JSON to CSV",
            "PDF to Text",
            "Images to PDF",
            "TXT to DOCX",
            "TXT to HTML"
        ]
    )

    if conversion_type == "Images to PDF":
        uploaded_files = st.file_uploader("Upload image files", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    else:
        uploaded_file = st.file_uploader("Upload file", type=None)

    if st.button("Convert"):
        if conversion_type == "CSV to Excel" and uploaded_file:
            out = csv_to_excel(uploaded_file)
            st.download_button("Download Excel File", open(out, "rb"), file_name="converted.xlsx")

        elif conversion_type == "Excel to CSV" and uploaded_file:
            out = excel_to_csv(uploaded_file)
            st.download_button("Download CSV File", open(out, "rb"), file_name="converted.csv")

        elif conversion_type == "JSON to CSV" and uploaded_file:
            out = json_to_csv(uploaded_file)
            if out:
                st.download_button("Download CSV File", open(out, "rb"), file_name="converted.csv")
            else:
                st.error("Invalid JSON format")

        elif conversion_type == "PDF to Text" and uploaded_file:
            out = pdf_to_text(uploaded_file)
            st.download_button("Download TXT File", open(out, "rb"), file_name="converted.txt")

        elif conversion_type == "Images to PDF" and uploaded_files:
            out = images_to_pdf(uploaded_files)
            st.download_button("Download PDF File", open(out, "rb"), file_name="converted.pdf")

        elif conversion_type == "TXT to DOCX" and uploaded_file:
            out = txt_to_docx(uploaded_file)
            st.download_button("Download DOCX File", open(out, "rb"), file_name="converted.docx")

        elif conversion_type == "TXT to HTML" and uploaded_file:
            out = txt_to_html(uploaded_file)
            st.download_button("Download HTML File", open(out, "rb"), file_name="converted.html")

        else:
            st.error("Please upload a file.")

if __name__ == "__main__":
    main()
