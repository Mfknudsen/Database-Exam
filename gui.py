import tkinter as tk
import requests
from llm import read_or_create_chat_history, write_to_db, create_new_chat

root = tk.Tk()
root.title("Warhammer lore chat bot")
root.geometry("800x600")

chat_history = read_or_create_chat_history("default_user_id")  # Initial user_id
chat_history_no = len(chat_history) - 1
conversation = chat_history[-1]["messages"]
conversation_id = chat_history[-1]["_id"]

def format_conversation(conversation):
    formatted = ""
    for entry in conversation:
        if entry['role'] != "system" and len(entry['content']) < 800:
            formatted += f"{entry['role']}: {entry['content']}\n"
    return formatted

def update_result_label():
    formatted_conversation = format_conversation(conversation)
    result_label.config(text=formatted_conversation)

def chat():
    query = query_entry.get()
    new_question = {'role': 'user', 'content': query}
    global conversation
    conversation.append(new_question)
    write_to_db(user_id, conversation_id, new_question)
    
    url = 'http://127.0.0.1:5000/chat'  # Change this if your Flask app runs on a different port
    data = {
        'query': query,
        'conversation': conversation,
        'chat_history_no': chat_history_no
    }
    response = requests.post(url, json=data)
    new_answer = {'role': 'assistant', 'content': response.json()}
    conversation.append(new_answer)
    write_to_db(user_id, conversation_id, new_answer)
    update_result_label()
    update_buttons()
def create_entry_with_label(root, label_text):
    frame = tk.Frame(root)
    frame.pack(pady=10)
    frame.pack()
    
    label = tk.Label(frame, text=label_text)
    label.pack(side="left")

    entry = tk.Entry(frame, width=70)
    entry.pack(side="left")
    
    return entry

def set_chat_history_no(number):
    global chat_history_no
    global conversation
    global conversation_id
    chat_history_no = number
    conversation_id = chat_history[number]["_id"]
    conversation = chat_history[number]["messages"]
    update_result_label()

def new_chat():
    global chat_history_no
    global chat_history
    global conversation
    global conversation_id
    print(len(chat_history))
    chat_history_no = len(chat_history)
    conversation_id = create_new_chat(user_id)
    chat_history = read_or_create_chat_history(user_id)
    conversation = chat_history[chat_history_no]["messages"]
    update_buttons()
    update_result_label()

def create_button(root, title, number):
    button = tk.Button(root, text=title, width=20, command=lambda: set_chat_history_no(number))
    button.pack(side="bottom", anchor="w", padx=10, pady=5)
    return button

def get_user():
    global user_id
    user_id = username_entry.get()
    update_user_data()

def update_user_data():
    global chat_history
    global chat_history_no
    global conversation
    global conversation_id

    chat_history = read_or_create_chat_history(user_id)
    chat_history_no = len(chat_history) - 1
    conversation = chat_history[-1]["messages"]
    conversation_id = chat_history[-1]["_id"]
    update_buttons()
    update_result_label()

username_entry = create_entry_with_label(root, "Write username: ")
username_button = tk.Button(root, text="Set Username", command=get_user)
username_button.pack()

query_entry = create_entry_with_label(root, "Ask away: ")

predict_button = tk.Button(root, text="Send", command=chat)
predict_button.pack()

formatted_conversation = format_conversation(conversation)
result_label = tk.Label(root, text=formatted_conversation, wraplength=300, justify="left", anchor="nw")
result_label.pack()

button_array = []
for index, chat_content_item in enumerate(chat_history):
    for chat_content in reversed(chat_content_item["messages"]):
        if chat_content.get('role') == 'user':
            last_user_content = chat_content.get('content')
            button = create_button(root, last_user_content[:25], index)
            button_array.append(button)
            break

def update_buttons():
    for button in button_array:
        button.destroy()
    button_array.clear() 
    
    for index, chat_content_item in enumerate(chat_history):
        for chat_content in reversed(chat_content_item["messages"]):
            if chat_content.get('role') == 'user':
                last_user_content = chat_content.get('content')
                button = create_button(root, last_user_content[:20], index)
                button_array.append(button)
                break

new_chat_button = tk.Button(root, text="Start new chat", command=new_chat)
new_chat_button.place(relx=0.97, rely=0.03, anchor='ne')

root.mainloop()
