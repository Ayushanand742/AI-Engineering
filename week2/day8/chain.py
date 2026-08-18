import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq 
from time import sleep

load_dotenv()
my_api_key= os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key not found")
client= Groq(api_key=my_api_key)

model = "openai/gpt-oss-20b"

JD = """
We are hiring a Backend python Devloper

Requirements
 - Strong python 
 - FastAPI or Django
 - Postgrade SQL
 - Docker
 - AWS
 - REST APIs
 - 2+ years of experience
"""

RESUME = """
Name= Ayush Anand

Experience:
3 years as a software developer

Skills:
Python, FastAPI, MySQL, Docker
REST APIs, Git

Projects:
Build a food delevery backend using 
Fast API and My SQL.

Deployed application using Docker
"""

def ask_llm(system_prompt, user_prompt):
    sys_msg= {
        "role": "system",
        "content": system_prompt
    }
    user_msg= {
        "role": "user",
        "content": user_prompt
    }
    messages= [sys_msg, user_msg]
    response=client.chat.completions.create(model= model, messages= messages)
    answer= response.choices[0].message.content
    return answer


def step1_res_extract():
    # extract skills from resume
    system_prompt = """
    You are a professional HR assistant. Extract the skills from the candidates resume provided.
    Only return the skills no other information. Do not invent any skills by yourself 
    """
    user_prompt = f"""
    Extract the skills form this resume
    {RESUME}
    """
    return ask_llm(system_prompt, user_prompt)

def step2_JD_extract():
    # extract skills from resume
    system_prompt = """
    You are a professional HR assistant. Extract the skills from the JD description provided.
    Only return the skills no other information. Do not invent any skills by yourself 
    """
    user_prompt = f"""
    Extract the skills form this JD
    {JD}
    """
    return ask_llm(system_prompt, user_prompt)

def step3_match(candidate, jd):
    system_prompt = """
    You are a professional HR assistant. Compare the skills from the JD and produce a final 
    score between 1 and 100 also produce a short verdict, weather the candidate is a good fit for the role 
    """
    user_prompt = f"""
    compare and match the skills
    JD:
    {jd}
    Candidate:
    {candidate}
    """
    return ask_llm(system_prompt, user_prompt)

candidate= step1_res_extract()
sleep(2)
jd= step2_JD_extract()
sleep(2)
score= step3_match(candidate, jd)
print(score)