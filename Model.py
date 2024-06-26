import os
from openai import OpenAI
from dotenv import load_dotenv
from pinecone import Pinecone

# Load config from a .env file:
dotenv_path = os.path.join(os.path.dirname(__file__), 'config.env')
load_dotenv(dotenv_path,verbose=True)

client = OpenAI(api_key=os.environ.get("OPENAI_KEY"))

# Connect to pinecone Lore Vector DB
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index("lore")

def get_embeddings(text):
    key = os.environ['OPENAI_KEY']
    client = OpenAI(api_key=key)
    return client.embeddings.create(input = [text], model="text-embedding-3-small").data[0].embedding


def vector_search(query, num_results=5, min_score=0.3):
    query_emb = get_embeddings(query)
    pipeline = index.query(
        vector=query_emb,
        top_k=num_results,
        include_values=False,
        include_metadata=True,
    )

    filtered_matches = [match for match in pipeline['matches'] if match['score'] >= min_score]

    pipeline['matches'] = filtered_matches
    
    return pipeline

def generate_response(conversation):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=150
    )
    return response.choices[0].message.content