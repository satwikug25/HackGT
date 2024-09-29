import base64
import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI


def encode_image(image_path):
    """Getting the base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def image_summarize(img_base64, prompt):
    """Make image summary"""
    chat = ChatOpenAI(model_name="gpt-4o")

    msg = chat.invoke(
        [
            HumanMessage(
                content=[
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"},
                    },
                ]
            )
        ]
    )
    return msg.content


def generate_img_summaries(path):
    """
    Generate summaries and base64 encoded strings for images
    path: Path to list of .jpg files extracted by Unstructured
    """

    # Store base64 encoded images
    img_base64_list = []

    # Store image summaries
    image_summaries = []

    # Prompt
    prompt = """ Analyze the provided medical image and give a detailed summary of your observations. 
        Include:   
            1.Type of medical image
            2.Body part or region shown.
            3.Any visible abnormalities or notable features.
            4.Potential diagnoses or areas that require further investigation, from the observations in step 3.
            5.Overall assessment of the image quality and any limitations in interpretation
        Provide your analysis in a clear, structured format suitable for medical professionals.
        """

    # Apply to images
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    base64_image = encode_image(path)
    img_base64_list.append(base64_image)
    summary = image_summarize(base64_image, prompt)
    chunks = text_splitter.split_text(summary)
    image_summaries.extend(chunks)

    return img_base64_list, image_summaries
