import tkinter as tk
import requests
from DBHandler import read_or_create_chat_history, write_answer_db, write_question_db, create_new_chat, create_new_user, login_db
from neo4jDB import suggest_topics, find_message_by_topic

def main_interface():
    root = tk.Tk()
    root.title("Warhammer lore chat bot")
    root.geometry("800x600")

    global chat_history
    global user_id
    chat_history = read_or_create_chat_history(user_id)
    global chat_history_no
    chat_history_no = len(chat_history) - 1
    global conversation
    conversation = chat_history[-1]["messages"]
    global conversation_id
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

    def chat(explore_query):
        query = ""
        original = True
        if explore_query:
            query = explore_query
            original = False
        else:
            query = query_entry.get()
        new_question = {'role': 'user', 'content': query}
        global conversation
        conversation.append(new_question)

        url = 'http://127.0.0.1:5003/chat'  # Change this if your Flask app runs on a different port
        data = {
            'query': query,
            'conversation': conversation,
            'chat_history_no': chat_history_no
        }
        response = requests.post(url, json=data)

        llm_response = response.json().get('llm_response')
        topic = response.json().get('topic')

        new_question['topic'] = topic

        write_question_db(conversation_id, new_question, original)
        new_answer = {'role': 'assistant', 'content': llm_response}
        conversation.append(new_answer)
        write_answer_db(conversation_id, new_answer)

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
        chat_history_no = len(chat_history)
        conversation_id = create_new_chat(user_id)
        chat_history = read_or_create_chat_history(user_id)
        conversation = chat_history[chat_history_no]["messages"]
        update_buttons()
        update_result_label()

    def explore(topic):
        query = find_message_by_topic(topic)
        new_chat()
        chat(query)

    def create_button(root, title, number):
        button = tk.Button(root, text=title, width=20, command=lambda: set_chat_history_no(number))
        button.pack(side="bottom", anchor="w", padx=10, pady=5)
        return button

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

    def create_explore_button(root, topic):
        button = tk.Button(root, text=topic, width=15, command=lambda: explore(topic))
        button.pack(anchor="e", side="bottom", padx=10, pady=5)
        return button
    
    suggested_topics = suggest_topics(str(user_id))
    for topic in suggested_topics:
        create_explore_button(root, topic['name'])

    query_entry = create_entry_with_label(root, "Ask away: ")

    predict_button = tk.Button(root, text="Send", command=lambda: chat(None))
    predict_button.pack()

    formatted_conversation = format_conversation(conversation)
    result_label = tk.Label(root, text=formatted_conversation, wraplength=300, justify="left", anchor="nw")
    result_label.pack()

    global button_array
    button_array = []
    for index, chat_content_item in enumerate(chat_history):
        for chat_content in reversed(chat_content_item["messages"]):
            if chat_content.get('role') == 'user':
                last_user_content = chat_content.get('content')
                button = create_button(root, last_user_content[:25], index)
                button_array.append(button)
                break

    new_chat_button = tk.Button(root, text="Start new chat", command=new_chat)
    new_chat_button.place(relx=0.97, rely=0.03, anchor='ne')

    root.mainloop()

def login_screen():
    login_root = tk.Tk()
    login_root.title("Login / Signup")
    login_root.geometry("800x600")

    def login():
        global username
        global user_id
        username_input = login_username_entry.get()
        if username_input:
            result = login_db(username_input)
            if result["status"] == "success":
                username = username_input
                user_id = result["user_id"]
                login_root.destroy()
                main_interface()
            else:
                error_label.config(text={result['message']})

    def signup():
        global username
        global user_id
        username_input = signup_username_entry.get()
        email = signup_email_entry.get()
        phone = signup_phone_entry.get()
        country = signup_country_entry.get()
        
        if username_input and email and phone and country:
            user_data = {
                "username": username_input,
                "email": email,
                "phone": phone,
                "country": country
            }
            result = create_new_user(user_data)
            if result["status"] == "success":
                username = username_input
                user_id = result["user_id"]
                login_root.destroy()
                main_interface()
            else:
                error_label.config(text=f"Signup Error: {result['message']}")

    def create_entry_with_label(root, label_text, width=30):
        frame = tk.Frame(root)
        frame.pack(pady=10)

        label = tk.Label(frame, text=label_text)
        label.pack(side="left")

        
        entry = tk.Entry(frame, width=width)

        entry.pack(side="left")

        return entry

    # Login section
    login_label = tk.Label(login_root, text="Login", font=("Helvetica", 14))
    login_label.pack(pady=10)

    login_username_entry = create_entry_with_label(login_root, "Username: ")

    login_button = tk.Button(login_root, text="Login", command=login)
    login_button.pack(pady=5)

    # Signup section
    signup_label = tk.Label(login_root, text="Signup", font=("Helvetica", 14))
    signup_label.pack(pady=10)

    signup_username_entry = create_entry_with_label(login_root, "Username: ")
    signup_email_entry = create_entry_with_label(login_root, "Email: ")
    signup_phone_entry = create_entry_with_label(login_root, "Phone: ")
    signup_country_entry = create_entry_with_label(login_root, "Country: ")

    signup_button = tk.Button(login_root, text="Signup", command=signup)
    signup_button.pack(pady=5)

    error_label = tk.Label(login_root, text="", fg="red")
    error_label.pack()

    login_root.mainloop()

login_screen()

if __name__ == "__main__":
    login_screen()
