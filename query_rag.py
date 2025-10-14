# rag_api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import requests
import json
from api import io  

app = FastAPI(title="RAG API")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_store = Chroma(
    collection_name="prompt_engineering",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

prompt_template = ChatPromptTemplate.from_template(
    """You are a helpful assistant that can answer questions about the blog post on prompt engineering.
    Use the following pieces of retrieved context to answer the question. 
    If you don’t know the answer, just say "I don’t know."

    Question: {question}
    Context: {context}
    """
)

class Query(BaseModel):
    question: str
    model: str = "deepseek-ai/DeepSeek-R1-0528"

@app.post("/ask")
def ask(query: Query):
    try:
        retrieved_docs = vector_store.similarity_search(query.question, k=3)
        docs_content = "\n".join([doc.page_content for doc in retrieved_docs])
        final_prompt = prompt_template.invoke({"question": query.question, "context": docs_content}).to_string()

        url = "https://api.intelligence.io.solutions/api/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": io
        }
        data = {
            "model": query.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": final_prompt}
            ]
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        result = response.json()
        text = result["choices"][0]["message"]["content"]

        return {"answer": text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
