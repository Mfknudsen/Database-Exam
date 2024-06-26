
import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from neo4jDB import create_conversation_node, create_user_node, create_message_node
from neo4j import GraphDatabase
from bson import ObjectId

dotenv_path = os.path.join(os.path.dirname(__file__), 'config.env')
load_dotenv(dotenv_path, verbose=True)

cluster = MongoClient(os.environ.get("MONGO_URI_CH"))

mydb = cluster["DBExam"]
conversationCollection = mydb["Conversations"]
userCollection = mydb["Users"]

uri = "bolt://localhost:7687"
user = "neo4j"
password = os.environ["NEO4J_PASSWORD"]

driver = GraphDatabase.driver(uri, auth=(user, password))

def read_or_create_chat_history(user_id):
    if not ObjectId.is_valid(user_id):
        print("Invalid user_id format")
        return {"status": "error", "message": "Invalid user_id format"}

    mongo_user_id = ObjectId(user_id)
    try:
        user_conversations = list(conversationCollection.find({"user_id": mongo_user_id}))

        if not user_conversations:
            result = new_conversation(user_id)
            if result["status"] == "success":
                user_conversations = [result["conversation"]]
            else:
                print(f"Error creating new conversation: {result.get('message')}")
                return result

        return user_conversations

    except Exception as error:
        print(f"MongoDB error: {str(error)}")
        return {"status": "error", "message": f"Error reading or creating chat history: {str(error)}"}


def login_db(username):
    try:
        user = userCollection.find_one({"username": username})
        if user:
            return {"status": "success", "user_id": user.get("_id")}
        else:
            print(f"User '{username}' not found")
            return {"status": "error", "message": "User not found"}
   
    except Exception as error:
        print(f"MongoDB error: {str(error)}")
        return {"status": "error", "message": f"Error logging in: {str(error)}"}


def write_answer_db(conversation_id, new_answer):
    if not ObjectId.is_valid(conversation_id):
        print("Invalid conversation_id format", conversation_id)
        return {"status": "error", "message": "Invalid conversation_id format"}

    mongo_conversation_id = ObjectId(conversation_id)
    try:
        conversationCollection.update_one(
            {"_id": mongo_conversation_id},
            {"$push": {"messages": new_answer}}
        )
        return {"status": "success"}

    except Exception as error:
        print(f"MongoDB error: {str(error)}")
        return {"status": "error", "message": f"Error writing answer to conversation in MongoDB: {str(error)}"}


def write_question_db(conversation_id, new_question, original):
    if not ObjectId.is_valid(conversation_id):
        return {"status": "error", "message": "Invalid user_id format"}

    mongo_conversation_id = ObjectId(conversation_id)
    try:
        with cluster.start_session() as mongo_session:
            with mongo_session.start_transaction():
                conversationCollection.update_one(
                    {"_id": mongo_conversation_id},
                    {"$push": {"messages": new_question}},
                )

                try:
                    with driver.session() as neo4j_session:
                        neo4j_session.write_transaction(
                            create_message_node, 
                            str(conversation_id), 
                            new_question['content'], 
                            new_question['role'], 
                            original,
                            new_question['topic']
                        )
                except Exception as neo4j_error:
                    mongo_session.abort_transaction()
                    print(f"Neo4j error: {str(neo4j_error)}")  # Print Neo4j error
                    return {"status": "error", "message": f"Error creating message node in Neo4j: {str(neo4j_error)}"}

                mongo_session.commit_transaction()
                return {"status": "success"}

    except Exception as mongo_error:
        print(f"MongoDB error: {str(mongo_error)}")  # Print MongoDB error
        return {"status": "error", "message": f"Error updating conversation in MongoDB: {str(mongo_error)}"}
    
def create_new_chat(user_id):
    result = new_conversation(user_id)
    if result["status"] == "success":
        conversation_id = result["conversation_id"]
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
                        neo4j_session.write_transaction(create_conversation_node, str(user_id), str(conversation_id))
                except Exception as neo4j_error:
                    mongo_session.abort_transaction()
                    print(f"Neo4j error: {str(neo4j_error)}")  # Print Neo4j error
                    return {"status": "error", "message": f"Error creating conversation node in Neo4j: {str(neo4j_error)}"}

                mongo_session.commit_transaction()
                return {
                    "status": "success",
                    "conversation_id": str(conversation_id),
                    "conversation": new_conversation_data
                }

            except Exception as mongo_error:
                mongo_session.abort_transaction()
                print(f"MongoDB error: {str(mongo_error)}")  # Print MongoDB error
                return {"status": "error", "message": f"Error inserting conversation in MongoDB: {str(mongo_error)}"}


def create_new_user(user):
    try:
        with cluster.start_session() as mongo_session:
            with mongo_session.start_transaction():
                user_id = userCollection.insert_one(user).inserted_id

                try:
                    with driver.session() as neo4j_session:
                        neo4j_session.write_transaction(create_user_node, user['username'], str(user_id))
                except Exception as neo4j_error:
                    mongo_session.abort_transaction()
                    print(f"Neo4j error: {str(neo4j_error)}")  # Print Neo4j error
                    return {"status": "error", "message": f"Error creating user node in Neo4j: {str(neo4j_error)}"}

                mongo_session.commit_transaction()
                return {"status": "success", "user_id": str(user_id)}

    except Exception as mongo_error:
        print(f"MongoDB error: {str(mongo_error)}")  # Print MongoDB error
        return {"status": "error", "message": f"Error inserting user in MongoDB: {str(mongo_error)}"}


