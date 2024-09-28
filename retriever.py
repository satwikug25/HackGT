import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import requests
import pdfplumber
from PIL import Image
import torch
import clip
import io




# Step 1: Download the PDF
url = "https://web.stanford.edu/class/archive/cs/cs161/cs161.1168/lecture1.pdf"
response = requests.get(url)
pdf_file = io.BytesIO(response.content)

# Step 2: Extract Images from the PDF
def extract_images_from_pdf(pdf_file):
    images = []
    with pdfplumber.open(pdf_file) as pdf:
        for page_number, page in enumerate(pdf.pages):
            for image in page.images:
                # Extract image bytes
                base_image = page.crop((image['x0'], image['top'], image['x1'], image['bottom']))
                img = base_image.to_image(resolution=150)
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                images.append({'image_data': img_byte_arr, 'page_number': page_number})
    return images

images = extract_images_from_pdf(pdf_file)

# Step 3: Load CLIP Model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Initialize Vector Store
vectorstore = InMemoryVectorStore()

# Step 4: Generate and Add Image Embeddings
for img_info in images:
    image_data = img_info['image_data']
    page_number = img_info['page_number']
    image = Image.open(io.BytesIO(image_data))
    image_input = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image_input)
    image_features = image_features.cpu().numpy().flatten()
    metadata = {'page_number': page_number, 'content_type': 'image'}
    vectorstore.add_embeddings([image_features], [{'page_content': 'Image', 'metadata': metadata}])

# Step 5: Process Text and Generate Text Embeddings Using CLIP
def get_retriever():
    # Load and split the PDF text
    loader = WebBaseLoader(
        web_paths=(
            url,
        ),
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                class_=("post-content", "post-title", "post-header")
            )
        ),
    )
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    for doc in splits:
        text = doc.page_content
        text_tokens = clip.tokenize(text).to(device)
        with torch.no_grad():
            text_features = model.encode_text(text_tokens)
        text_features = text_features.cpu().numpy().flatten()
        metadata = {'content_type': 'text'}
        vectorstore.add_embeddings([text_features], [{'page_content': text, 'metadata': metadata}])

    retriever = vectorstore.as_retriever()
    return retriever

retriever = get_retriever()
