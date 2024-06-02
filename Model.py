import os
from openai import OpenAI
from dotenv import load_dotenv
import pymongo

# Load config from a .env file:
dotenv_path = os.path.join(os.path.dirname(__file__), 'config.env')
load_dotenv(dotenv_path,verbose=True)
MONGODB_URI = os.environ["MONGO_URI"]

# Connect to your MongoDB cluster:
client = pymongo.MongoClient(MONGODB_URI)

# Get a reference to the "sample_mflix" database:
db = client["cluster0"]

# Get a reference to the "movies" collection:
collection = db["40klore"]

def get_embeddings(text):
    key = os.environ['OPENAI_KEY']
    client = OpenAI(api_key=key)
    return client.embeddings.create(input = [text], model="text-embedding-3-small").data[0].embedding


def vector_search(query, num_results=10):
    query_emb = get_embeddings(query)
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_emb,
                "numCandidates": 200,
                "limit": num_results
            }
        }
    ]
    return collection.aggregate(pipeline)

if __name__ == '__main__':
    query = "Who led the 13th black crusade?"

    results = vector_search(query)

    for doc in results:
        print(" * {title}, {content}, {url}".format(
            title=doc["title"],
            content=doc["content"],
            url=doc["url"],
    ))