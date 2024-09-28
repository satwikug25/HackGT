import io

import requests
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai.embeddings import OpenAIEmbeddings
from PyPDF2 import PdfReader


def fetch_pdf_from_url(url):
    response = requests.get(url)
    return io.BytesIO(response.content)


def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def get_retriever():
    pdf_url = "https://web.stanford.edu/class/archive/cs/cs161/cs161.1168/lecture1.pdf"
    pdf_file = fetch_pdf_from_url(pdf_url)
    text = extract_text_from_pdf(pdf_file)

    # Split the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)

    # Create documents
    documents = [
        Document(page_content=chunk, metadata={"source": pdf_url}) for chunk in chunks
    ]

    # Initialize the vector store
    embeddings = OpenAIEmbeddings()  # Make sure to set your OpenAI API key
    vector_store = InMemoryVectorStore(embedding=embeddings)

    # Add documents to the vector store
    vector_store.add_documents(documents)

    return vector_store.as_retriever()
