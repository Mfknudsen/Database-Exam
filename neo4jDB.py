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

def create_message_node(tx, conversation_id, content, role, original, topic):
    query = (
        "MATCH (c:Conversation {conversation_id: $conversation_id}) "
        "CREATE (c)-[:HAS_MESSAGE {role: $role, original: $original}]->(m:Message {content: $content}) "
        "WITH c, m "
        "MERGE (t:Topic {name: $topic}) "
        "MERGE (m)-[:ABOUT]->(t) "
        "RETURN m"
    )
    result = tx.run(query, conversation_id=conversation_id, content=content, role=role, original=original, topic=topic)
    return result.single()[0]

def suggest_topics(user_id):
    with driver.session() as session:
        result = session.read_transaction(_find_similar_users_topics, user_id)
        return result

def _find_similar_users_topics(tx, user_id):
    query = """
    MATCH (u:User {user_id: $user_id})-[:HAS_CONVERSATION]->(:Conversation)-[:HAS_MESSAGE]->(:Message)-[:ABOUT]->(t:Topic)
    WITH u, collect(t) AS userTopics

    MATCH (u)-[:HAS_CONVERSATION]->(:Conversation)-[:HAS_MESSAGE]->(:Message)-[:ABOUT]->(commonTopic:Topic)<-[:ABOUT]-(:Message)<-[:HAS_MESSAGE]-(:Conversation)<-[:HAS_CONVERSATION]-(otherUser:User)
    WHERE otherUser.user_id <> $user_id
    WITH userTopics, otherUser

    MATCH (otherUser)-[:HAS_CONVERSATION]->(:Conversation)-[:HAS_MESSAGE]->(:Message)-[:ABOUT]->(suggestedTopic:Topic)
    WHERE NOT suggestedTopic IN userTopics
    RETURN DISTINCT suggestedTopic.name AS suggestedTopic
    LIMIT 3
    """
    result = tx.run(query, user_id=user_id)
    return [{"name": record["suggestedTopic"]} for record in result]

def find_message_by_topic(topic_name):
    with driver.session() as session:
        result = session.read_transaction(_find_message_by_topic, topic_name)
        return result

def _find_message_by_topic(tx, topic_name):
    query = """
    MATCH (t:Topic {name: $topic_name})<-[:ABOUT]-(m:Message)
    RETURN m.content AS message
    LIMIT 1
    """
    result = tx.run(query, topic_name=topic_name)
    record = result.single()
    return record["message"] if record else None