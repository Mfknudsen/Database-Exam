from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), 'config.env')
load_dotenv(dotenv_path,verbose=True)

uri = "bolt://localhost:7687"
user = "neo4j"
password = os.environ["NEO4J_PASSWORD"]

driver = GraphDatabase.driver(uri, auth=(user, password))

def create_user_node(tx, username, user_id):
    query = (
        "CREATE (u:User {username: $username, user_id: $user_id}) "
        "RETURN u"
    )
    result = tx.run(query, username=username, user_id=user_id)
    return result.single()[0]

def create_conversation_node(tx, user_id, conversation_id):
    query = (
        "MATCH (u:User {user_id: $user_id}) "
        "CREATE (u)-[:HAS_CONVERSATION]->(c:Conversation {conversation_id: $conversation_id}) "
        "RETURN c"
    )
    result = tx.run(query, user_id=user_id, conversation_id=conversation_id)
    return result.single()[0]

def create_message_node(tx, conversation_id, content, role, original):
    query = (
        "MATCH (c:Conversation {conversation_id: $conversation_id}) "
        "CREATE (c)-[:HAS_MESSAGE {role: $role, original: $original}]->(m:Message {content: $content}) "
        "RETURN m"
    )
    result = tx.run(query, conversation_id=conversation_id, content=content, role=role, original=original)
    return result.single()[0]

