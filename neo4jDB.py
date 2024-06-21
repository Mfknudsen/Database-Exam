from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), 'config.env')
load_dotenv(dotenv_path,verbose=True)

uri = "bolt://localhost:7687"
user = "neo4j"
password = os.environ["NEO4J_PASSWORD"]

driver = GraphDatabase.driver(uri, auth=(user, password))

def create_user(username):
    with driver.session() as session:
        session.write_transaction(_create_user_node, username)

def _create_user_node(tx, username):
    query = (
        "CREATE (u:User {username: $username}) "
        "RETURN u"
    )
    result = tx.run(query, username=username)
    return result.single()[0]

def create_conversation(username):
    with driver.session() as session:
        session.write_transaction(_create_conversation_node, username)

def _create_conversation_node(tx, username):
    query = (
        "MATCH (u:User {username: $username}) "
        "CREATE (u)-[:HAS_CONVERSATION]->(c:Conversation) "
        "RETURN c"
    )
    result = tx.run(query, username=username)
    return result.single()[0]

