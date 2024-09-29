import io

import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader


def fetch_pdf_from_url(url):
    response = requests.get(url)
    return io.BytesIO(response.content)


def extract_text_from_pdf(pdf_file):
    pdfFileObject = open("Lumbar_Puncture_Surgical_Plan.pdf", "rb")
    pdf_reader = PdfReader(pdfFileObject)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def get_chunks():
    pdf_url = "https://drive.google.com/file/d/1raeUWULDtRkMEDaJyJoSnAX4QNtPqgEE/view?usp=sharing"
    pdf_file = fetch_pdf_from_url(pdf_url)
    text = extract_text_from_pdf(pdf_file)

    # Split the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    return chunks
