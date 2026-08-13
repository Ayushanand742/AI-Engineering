import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq 

load_dotenv()
my_api_key= os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key not found")
client= Groq(api_key=my_api_key)

model= "llama-3.3-70b-versatile"


def llm_ans(prompt):
    message= {
        "role": "user",
        "content": prompt
    }
    messages= [message]
    # response= client.chat.completions.create(model= model, messages= message)
    response = client.chat.completions.create(
    model=model,
    messages=messages
)
    answer= response.choices[0].message.content
    return answer


bad_prompt=""""
# ROLE: 
you are a support assistant at a mobile/laptop compnay
# Task:
you have to classify the issue in a category
# CONSTRANT:
you have to classify the issue in one of the three categories namely billing, techinical, return
This is a user complaint:
My laptop is not working 
"""
print(llm_ans(bad_prompt ))