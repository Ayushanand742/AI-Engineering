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




# Structure it
from pydantic import BaseModel
class Ticket(BaseModel):
    name: str
    email: str
    issue: str

schema = Ticket.model_json_schema()

response_format = {
    "type": "json_object"
}

system_prompt = f"""
Extract the personal information from the ticket strictly based on the schema below and return the result as JSON.
{schema}
"""

message_system= {
    "role": "system",
    "content": system_prompt
}

message_user= {
    "role": "user",

}

text= "Hello my name is Ayush Anand. I have a phone which is not working at all. My address is Deoghar. My email is itz.ayushanand@gmail.com. My contact no is 6207636492"
prompt= f""""
This is a customer ticket. Please extract the personal information from this.
{text}
"""
message= {
    "role": role,
    "content":prompt 
}

messages= [message_system, message]

response= client.chat.completions.create(model=model, messages=messages, response_format= response_format)


ansrwe= response.choices[0].message.content
print(ansrwe)

# how to reaed jason
import json
raw_json= ansrwe
data_file= json.loads(raw_json)
ticket= Ticket(**data_file)

# pass these to read the data

print(ticket.name)
print(ticket.email)
print(ticket.issue)