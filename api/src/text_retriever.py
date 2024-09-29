import io

import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader


def extract_text_from_pdf(file_path):
    pdfFileObject = open(file_path, "rb")
    pdf_reader = PdfReader(pdfFileObject)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def get_chunks(file_path):
    text = extract_text_from_pdf(file_path)

    # Split the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    return chunks
