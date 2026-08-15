import os
import re
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq 
from time import sleep

load_dotenv()
my_api_key= os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key not found")
client= Groq(api_key=my_api_key)

model= "llama-3.3-70b-versatile"

# Tools

def get_product_price(product):
    if product == "iphone 17":
        return 1000
    elif product == "iphone 15":
        return 500
    else:
        return 0

def calculator(expression):
    try:
        return eval(expression)
    except:
        return "calc error!"

tools= {
    "get_product_price": get_product_price,
    "calculator": calculator
}
system_promt= """"
You are a shoping assistant
you have these tools:
get_product_price(product)
calculator(calculator)

IMPORTANT:
call tools  exactly like these examples: 

Action: get_product_price("iphone 17")
Action: calculator("5000 - 1000")

Never write:
get_product_price(product= "iphone 17")

Never write:
calculator(expression= "5000 - 1000")
Follow these rules:

1. Decide what you need to do next.
2. Call only one tool at a time.
3. After writing an Action, STOP immediately.
4. Never guess or invent a tool result.
5. Wait until you receive an Observation.
6. Then decie your next action.
7. When the task is complete, give the Final Answer.

Format:

Thought: whart you need to do
Action: tool_name(argument)

When finished:

Final Answer: your answer
"""

def run_agent(question):

    message= [
        {
            "role": "system",
            "content": system_promt
        },
        {
            "role": "user",
            "content": question
        }   
    ]
    for step in range(5):

        print("\n---------------")
        print("STEP", step + 1)

        response= client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=message,
            temperature=0
        )

        answer= response.choices[0].message.content

        print(answer)

        # Agent has finished
        if "Final Answer:" in answer:
            break

        # Find the Action
        match = re.search(r'Action:\s*(\w+)\((.*?)\)', answer)

        if match:
            tool_name= match.group(1)

            tool_input= match.group(2)

            tool_input= tool_input.strip()

            tool_input= tool_input.strip('"')

            # Run the tool
            if tool_name in tools:

                tool= tools[tool_name]

                observation= tool(tool_input)

            else:
                observation= "Tool not found"

            print(
                "observation:",
                observation
            )

            # Add LLM responce to mwmory
            message.append({
                "role": "assistant",
                "content": answer
            })
            # Give tool result back to LLM
            message.append({
                "role": "user",
                "content": 
                "observation:"
                + str(observation)
            })
            sleep(5)

prompt= """
I have 5000  rupees. What is the price of an iphone 17?
and how much money will I have left?
"""
run_agent(prompt)