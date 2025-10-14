from langchain_core.prompts import ChatPromptTemplate
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
import requests
import json
import os
from api import io


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_store = Chroma(
    collection_name="prompt_engineering",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)


prompt = ChatPromptTemplate.from_template(
    """You are a helpful assistant that can answer questions about the blog post on prompt engineering.
    Use the following pieces of retrieved context to answer the question. 
    If you don’t know the answer, just say "I don’t know."

    Question: {question}
    Context: {context}
    """
)

question = "What is prompt engineering?"
retrieved_docs = vector_store.similarity_search(question, k=3)
docs_content = "\n".join([doc.page_content for doc in retrieved_docs])

final_prompt = prompt.invoke({"question": question, "context": docs_content}).to_string()

# url
url = "https://api.intelligence.io.solutions/api/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": io
}

data = {
    "model": "deepseek-ai/DeepSeek-R1-0528",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": final_prompt}
    ]
}

response = requests.post(url, headers=headers, json=data)

if response.status_code != 200:
    print("Error:", response.text)
else:
    result = response.json()
    try:
        text = result["choices"][0]["message"]["content"]
        text = text.split('/think')[1][2:]
        print("Answer:", text)
    except Exception as e:
        print("Unexpected response format:", json.dumps(result, indent=2))
