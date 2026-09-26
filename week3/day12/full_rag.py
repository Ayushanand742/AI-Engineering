import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import numpy as np
from sentence_transformers import SentenceTransformer
import sys

model = SentenceTransformer("all-MiniLM-L6-v2")

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client=Groq(api_key=my_api_key)
groqmodel = "openai/gpt-oss-120b"


documents= [
    "Employees recieve 24 days of paid leave per year.",

    "Empolyees work form office on Tuesday, Wednesday, and Thrusday."
    "Monday and friday are optional, work form home days",

    "Employees recieve ₹3000 mer month for gym reimbursment"

    "Employees can clame ₹2000 mer month for home internet"

    "Employees have 90 days notice period"
]

document_embeddings= model.encode(documents)
print(sys.getsizeof(document_embeddings))

def cosine_similarity(a,b):
    return np.dot(a,b)/ (
        np.linalg.norm(a) * np.linalg.norm(b)
    )

def retrieve(query_embeddings):
    scores= []
    for i, document in enumerate(document_embeddings):
        score= cosine_similarity(query_embeddings, document)
        scores.append((score, documents[i]))
    scores.sort(reverse= True)
    return scores[0]

def ask_llm(question, context):
    sys_prompt=f"""answer in one line only. Answer only based on this context. do not hallucinate. Context: {context}"""
    system_message={
        "role": "system",
        "content": sys_prompt

    }
    message={
        "role": "user",
        "content": question
    }
    messages=[system_message, message]
    response=client.chat.completions.create(model=groqmodel, messages=messages)
    answer=response.choices[0].message.content
    return answer

query= "HOw much vacation do I get?"
query_embeddings= model.encode(query)
score, context= retrieve(query_embeddings)
answer= ask_llm(query, context)
print(answer)


