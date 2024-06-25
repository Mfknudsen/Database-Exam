
import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from neo4jDB import create_conversation_node, create_user_node
from neo4j import GraphDatabase
from bson import ObjectId

dotenv_path = os.path.join(os.path.dirname(__file__), 'config.env')
load_dotenv(dotenv_path, verbose=True)

cluster = MongoClient(os.environ.get("MONGO_URI_CH"))

mydb = cluster["DBExam"]
conversationCollection = mydb["Conversations"]
messagesCollection = mydb["Messages"]
userCollection = mydb["Users"]

uri = "bolt://localhost:7687"
user = "neo4j"
password = os.environ["NEO4J_PASSWORD"]

driver = GraphDatabase.driver(uri, auth=(user, password))

def read_or_create_chat_history(user_id):
    if not ObjectId.is_valid(user_id):
        return {"status": "error", "message": "Invalid user_id format"}

    mongo_user_id = ObjectId(user_id)
    user_conversations = list(conversationCollection.find({"user_id": mongo_user_id}))

    if not user_conversations:
        result = new_conversation(user_id)
        if result["status"] == "success":
            user_conversations = [result["conversation"]]
        else:
            return result

    return user_conversations


def write_to_db(conversation_id, new_entry):
    conversationCollection.update_one(
        {"_id": conversation_id},
        {"$push": {"messages": new_entry}}
    )

def create_new_chat(user_id):
    result = new_conversation(user_id)
    if result["status"] == "success":
        conversation_id = [result["conversation_id"]]
        return conversation_id
    else:
        return result

def new_conversation(user_id):
    if not ObjectId.is_valid(user_id):
        return {"status": "error", "message": "Invalid user_id format"}

    mongo_user_id = ObjectId(user_id)

    initial_message = {
        "role": "system",
        "content": "You are a helpful chatbot that answers the users questions. You will be given source material and chat history and you are to only answer the last user question given, grounded in the documents you are given. If the answer is not in the documents do not answer"
    }
    new_conversation_data = {
        "user_id": mongo_user_id,
        "messages": [initial_message]
    }

    with cluster.start_session() as mongo_session:
        with mongo_session.start_transaction():
            try:
                conversation_id = conversationCollection.insert_one(new_conversation_data).inserted_id

                try:
                    with driver.session() as neo4j_session:
                        neo4j_session.write_transaction(create_conversation_node, user_id, str(conversation_id))
                except Exception as neo4j_error:
                    mongo_session.abort_transaction()
                    return {"status": "error", "message": f"Error creating conversation node in Neo4j: {str(neo4j_error)}"}

                mongo_session.commit_transaction()
                return {
                    "status": "success",
                    "conversation_id": str(conversation_id),
                    "conversation": new_conversation_data
                }

            except Exception as mongo_error:
                mongo_session.abort_transaction()
                return {"status": "error", "message": f"Error inserting conversation in MongoDB: {str(mongo_error)}"}


def create_new_user(user):
    try:
        if not user:
            return {"status": "error", "message": "User data is empty"}
        
        with cluster.start_session() as mongo_session:
            with mongo_session.start_transaction():
                user_id = userCollection.insert_one(user).inserted_id

                try:
                    with driver.session() as neo4j_session:
                        neo4j_session.write_transaction(create_user_node, user['username'], str(user_id))
                except Exception as neo4j_error:
                    mongo_session.abort_transaction()
                    return {"status": "error", "message": f"Error creating user node in Neo4j: {str(neo4j_error)}"}

                mongo_session.commit_transaction()
                return {"status": "success", "user_id": str(user_id)}

    except Exception as mongo_error:
        return {"status": "error", "message": f"Error inserting user in MongoDB: {str(mongo_error)}"}
