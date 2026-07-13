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
# 3 prompts
prompt1= "Hi"
prompt2= "Explain time travel in detail"
prompt3= "Write a 100 word essay on Mechine Learning"

prompts= [prompt1, prompt2, prompt3]
for prompt in prompts:
    message= {
    "role": role,
    "content":prompt
    }
    messages= [message]
    response= client.chat.completions.create(model=model, messages=messages, max_tokens=50)
    usage= response.usage
    print(f"Prompt:{prompt} -->ypur tokens: {usage.prompt_tokens} completion_tokens: {usage.completion_tokens} total tokens: {usage.total_tokens}Finish Resion: {response.choices[0].finish_reason}")


# prompt= "Hi my name is ayush"
# # SYSTEM
# message_system= {
#     "role": "system",
#     "content": "You are a brand manager who suggest name for my food brand suggest one name only"
# }
# # message me role and content
# message= {
#     "role": role,
#     "content":prompt
# }

#messages= [message_system,message]

#response= client.chat.completions.create(model=model, messages=messages,)
