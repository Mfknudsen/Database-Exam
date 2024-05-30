import os
import json
from openai import OpenAI
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'config.env')
load_dotenv(dotenv_path,verbose=True)

client = OpenAI(api_key=os.environ.get("OPENAI_KEY"))

def read_or_create_chat_history(directory):
   
    if not os.path.exists(directory):
        os.makedirs(directory)  

    files = os.listdir(directory)
    
    if not files:
        with open(os.path.join(directory, 'chat_history_0.txt'), 'w') as file:
            file.write('''[
{
    "role": "system",
    "content": "You are a helpful chatbot that answers the users questions. You will be given source material and chat history and you are to only answer the last user question given, grounded in the documents you are given. If the answer is not in the documents do not answer"
}
]''')
        files = os.listdir(directory)
    
    files.sort()

    file_contents = []
    
    for file_name in files:
        with open(os.path.join(directory, file_name), 'r') as file:
            contents = json.load(file)
            file_contents.append(contents)
                
    return file_contents

def write_to_file(directory, number, new_entry):
    file_path = os.path.join(directory, f"chat_history_{number}.txt")
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []
    
    data.append(new_entry)
    
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def create_new_chat(directory, number):
    with open(os.path.join(directory, f'chat_history_{number}.txt'), 'w') as file:
        file.write('''[
{
    "role": "system",
    "content": "You are a helpful chatbot that answers the users questions. You will be given source material and chat history and you are to only answer the question grounded in the documents you are given. If the answer is not in the documents do not answer"
}
]''')

def generate_response(conversation):
    print(conversation)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=150
    )
    return response.choices[0].message.content
