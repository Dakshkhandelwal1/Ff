# -*- coding: utf-8 -*-
"""Script.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VMYZnHk9DAiiuqwYn8wZcD9RRO9YhgrU
"""

!pip install pyPDF2

import PyPDF2

def extract_text_from_pdfs(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

# Example usage
pdf_file_path = "/content/28345af3-7271-4146-8cf3-8da0f9c73222.pdf"
extracted_text = extract_text_from_pdfs(pdf_file_path)
print(len(extracted_text))

!pip install pyPDF2
!pip install streamlit
!pip install Sentence_Transformer
!pip install chromadb
!pip install langchain
!pip install langchain_community
!pip install dotenv
!pip install litellm
#!pip install Arvix
import os
import PyPDF2
import streamlit as st
from sentence_transformers import SentenceTransformer
import chromadb
from litellm import completion
from langchain.text_splitter import RecursiveCharacterTextSplitter
#from langchain_community.tools import ArxivQueryRun
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("your gemini api key")
huggingface_token = os.getenv("your huggingface token")



client = chromadb.PersistentClient(path="chroma_db")



from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", token="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")  # Replace with your actual token

def process_text_and_store(all_text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50, separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_text(all_text)
    try:
        client.delete_collection(name="knowledge_base")
    except Exception:
        pass

    collection = client.create_collection(name="knowledge_base")

    for i, chunk in enumerate(chunks):
        # text_embedding_model is not defined. Assuming you have a model instance available.
        # Alternatively, you might need to load or initialize the model here.
        embedding = model.encode(chunk)
        collection.add(
            ids=[f"chunk_{i}"],
            embeddings=[embedding.tolist()],
            metadatas=[{"source": "pdf", "chunk_id": i}],
            documents=[chunk]
        )
    return collection

def semantic_search(query, collection, top_k=2):
    query_embedding = model.encode(query) # This line and the lines below were not indented properly
    results = collection.query(
        query_embeddings=[query_embedding.tolist()], n_results=top_k
    )
    return results

def generate_response(query, context):
    prompt = f"Query: {query}\nContext: {context}\nAnswer:"
    response = completion(
        model="gemini/gemini-1.5-flash",
        messages=[{"content": prompt, "role": "user"}],
        api_key="AIzaSyCUtKi8jDhD9qxNG-YjyGgO-02-U42wJFo"
    )
    return response['choices'][0]['message']['content']

all_text = extract_text_from_pdfs("/content/28345af3-7271-4146-8cf3-8da0f9c73222.pdf")

def main():
    st.title("RAG-powered Research Paper Assistant")

    # Option to choose between PDF upload and arXiv search
    option = st.radio("Choose an option:", ("start", "Search arXiv"))

    if option == "start":

      st.write("Processing uploaded files...")
      #extracted_text = extract_text_from_pdfs("/content/28345af3-7271-4146-8cf3-8da0f9c73222.pdf")
      collection = process_text_and_store(extracted_text)
      st.success("PDF content processed and stored successfully!")

      query = st.text_input("Enter your query:")
      if st.button("Execute Query") and query:
        results = semantic_search(query, collection)
        context = "\n".join(results['documents'][0])
        response = generate_response(query, context)
        st.subheader("Generated Response:")
        st.write(response)

    elif option == "Search arXiv":
        pass
