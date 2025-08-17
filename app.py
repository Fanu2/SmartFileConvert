import streamlit as st
import pandas as pd
import pdfplumber
from PIL import Image
from fpdf import FPDF
from docx import Document

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
    df = pd.read_json(file)
    output_path = "output.csv"
    df.to_csv(output_path, index=False)
    return output_path

def pdf_to_text(file):
    output_path = "output.txt"
    with pdfplumber.open(file) as pdf, open(output_path, "w", encoding="utf-8") as out:
        for page in pdf.pages:
            out.write(page.extract_text() + "\n")
    return output_path

def images_to_pdf(files):
    image_list = []
    for file in files:
        img = Image.open(file)
        img = img.convert("RGB")
        image_list.append(img)
    output_path = "output.pdf"
    if image_list:
        image_list[0].save(output_path, save_all=True, append_images=image_list[1:])
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

    st.write("Upload your file(s):")

    if conversion_type == "Images to PDF":
        uploaded_files = st.file_uploader("Upload multiple image files", type=["jpg", "png"], accept_multiple_files=True)
    else:
        uploaded_file = st.file_uploader("Upload a file", type=None)

    if st.button("Convert"):
        if conversion_type == "CSV to Excel" and uploaded_file:
            out = csv_to_excel(uploaded_file)
            st.download_button("Download Excel File", open(out, "rb"), file_name="converted.xlsx")

        elif conversion_type == "Excel to CSV" and uploaded_file:
            out = excel_to_csv(uploaded_file)
            st.download_button("Download CSV File", open(out, "rb"), file_name="converted.csv")

        elif conversion_type == "JSON to CSV" and uploaded_file:
            out = json_to_csv(uploaded_file)
            st.download_button("Download CSV File", open(out, "rb"), file_name="converted.csv")

        elif conversion_type == "PDF to Text" and uploaded_file:
            out = pdf_to_text(uploaded_file)
            st.download_button("Download Text File", open(out, "rb"), file_name="converted.txt")

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
            st.error("Please upload a file!")

if __name__ == "__main__":
    main()
