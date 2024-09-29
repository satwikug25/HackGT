import uuid

from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.storage import InMemoryStore
from langchain_core.documents import Document


def create_multi_vector_retriever(vectorstore, chunks, source, image_summaries):
    """
    Create retriever that indexes summaries, but returns raw images or texts
    """
    documents = [
        Document(page_content=chunk, metadata={"source": source}) for chunk in chunks
    ]
    vectorstore.add_documents(documents)
    image_docs = [Document(page_content=chunk) for chunk in image_summaries]
    vectorstore.add_documents(image_docs)
    return vectorstore.as_retriever()
