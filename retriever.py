import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from PIL import Image


def get_retriever():
    # Load and split the PDF text
    url = "https://web.stanford.edu/class/archive/cs/cs161/cs161.1168/lecture1.pdf"
    loader = WebBaseLoader(
        web_paths=(url,),
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                class_=("post-content", "post-title", "post-header")
            )
        ),
    )
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = InMemoryVectorStore(embedding=OpenAIEmbeddings())
    vectorstore.add_documents(splits)
    retriever = vectorstore.as_retriever()
    return retriever
