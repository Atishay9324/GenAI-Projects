from dotenv import load_dotenv
from google import genai
from google.genai import types
from Persona_prompt import Persona_Prompt # this is the system prompt you provided

import os
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

chat = client.chats.create(model="gemini-2.0-flash", config=types.GenerateContentConfig(
        system_instruction = Persona_Prompt,))

def generate_response():
    question = input("Ask a question or type 'end chat' to exit: ")
    if question != "end chat":
        response = chat.send_message(question)


        for message in chat.get_history():
                print(f'role - {message.role}',end=": ")
                print(message.parts[0].text)
        
        generate_response()

    else:
        print("Chat ended.")
    
generate_response()
