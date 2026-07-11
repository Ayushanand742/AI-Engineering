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
role= "user"
prompt= "suggest a name for my food brand"

# SYSTEM
message_system= {
    "role": "system",
    "content": "You are a brand manager who suggest name for my food brand suggest one name only"
}
# message me role and content
message= {
    "role": role,
    "content":prompt 
}

messages= [message_system,message]
# Temprature is by defalut is 0 meaning safe. range is [0,2]
response= client.chat.completions.create(model=model, messages=messages, temperature=2)
# print(response)

ansrwe= response.choices[0].message.content
print(ansrwe)