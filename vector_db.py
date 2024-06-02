import os
from dotenv import load_dotenv
import pandas as pd
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
import uuid

dotenv_path = 'config.env'
load_dotenv(dotenv_path,verbose=True)
OPENAI_KEY = os.environ["OPENAI_KEY"]
PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]

pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "units"

file_path = "Document - Lore/data.csv"

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536, 
        metric="cosine", 
        spec=ServerlessSpec(
            cloud="aws", 
            region="us-east-1"
        ) 
    ) 

index = pc.Index(index_name)

csv = pd.read_csv(file_path, sep=">").head(20)

def get_embeddings(text):
    key = os.environ['OPENAI_KEY']
    client = OpenAI(api_key=key)
    return client.embeddings.create(input = [text], model="text-embedding-3-small").data[0].embedding 

data_to_upsert = [
    { 
        "id": str(uuid.uuid4()), #Ved ikke lige hvad vi skal bruge som id, man skal umiddelbart manuelt tilføje det.
        "values": get_embeddings(row[1]["text"]), 
        "metadata": {
            'title': row[1]['title'], 
            'url': row[1]['url'], 
            'content': row[1]["text"],
            "chunk_id": row[1]["chunk_id"],
        }
    }
    for row in csv.iterrows()
]


if __name__ == '__main__':
    index.upsert(vectors=data_to_upsert)