import os
from openai import OpenAI
from dotenv import load_dotenv
import pymongo
from pinecone import Pinecone

# Load config from a .env file:
dotenv_path = os.path.join(os.path.dirname(__file__), 'config.env')
load_dotenv(dotenv_path,verbose=True)
MONGODB_URI = os.environ["MONGO_URI_CH"]

# Connect to your MongoDB cluster:
client = pymongo.MongoClient(MONGODB_URI)

# Connect to pinecone
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index("units")

# Get a reference to the "sample_mflix" database:
db = client["cluster0"]

# Get a reference to the "movies" collection:
collection = db["40klore"]

def get_embeddings(text):
    key = os.environ['OPENAI_KEY']
    client = OpenAI(api_key=key)
    return client.embeddings.create(input = [text], model="text-embedding-3-small").data[0].embedding


def vector_search(query, num_results=5):
    query_emb = get_embeddings(query)
    pipeline = index.query(
        vector=query_emb,
        top_k=num_results,
        include_values=False,
        include_metadata=True,
    )
    return pipeline