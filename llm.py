
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from neo4jDB import create_conversation, create_user

dotenv_path = os.path.join(os.path.dirname(__file__), 'config.env')
load_dotenv(dotenv_path, verbose=True)

client = OpenAI(api_key=os.environ.get("OPENAI_KEY"))

cluster = MongoClient(os.environ.get("MONGO_URI_CH"))

mydb = cluster["DBExam"]
conversationCollection = mydb["Conversations"]
messagesCollection = mydb["Messages"]
userCollection = mydb["Users"]

def read_or_create_chat_history(user_id):
    user_conversations = list(conversationCollection.find({"user_id": user_id}))
    
    if not user_conversations:
        initial_message = {
            "role": "system",
            "content": "You are a helpful chatbot that answers the users questions. You will be given source material and chat history and you are to only answer the last user question given, grounded in the documents you are given. If the answer is not in the documents do not answer"
        }
        new_conversation = {
            "user_id": user_id,
            "messages": [initial_message]
        }
        conversationCollection.insert_one(new_conversation)
        user_conversations = [new_conversation]

        create_conversation(user_id)
    
    return user_conversations

def write_to_db(conversation_id, new_entry):
    conversationCollection.update_one(
        {"_id": conversation_id},
        {"$push": {"messages": new_entry}}
    )

def create_new_chat(user_id):
    initial_message = {
        "role": "system",
        "content": "You are a helpful chatbot that answers the users questions. You will be given source material and chat history and you are to only answer the question grounded in the documents you are given. If the answer is not in the documents do not answer"
    }
    new_conversation = {
        "user_id": user_id,
        "messages": [initial_message]
    }
    conversation_id = conversationCollection.insert_one(new_conversation).inserted_id
    create_conversation(user_id)
    return conversation_id

def create_new_user(user):
    try:
        if user:
            user_id = userCollection.insert_one(user).inserted_id
            create_user(user_id)
            return {"status": "success", "user_id": user_id}
        else:
            return {"status": "error", "message": "User data is empty"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def generate_response(conversation):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=150
    )
    return response.choices[0].message.content
