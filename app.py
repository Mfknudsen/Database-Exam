import os
from flask import Flask, jsonify, request
from Model import vector_search
from llm import generate_response

app = Flask(__name__)


@app.route('/chat', methods=['POST'])
def predict():
    req = request.json
    query = req["query"]
    conversation = req["conversation"]

    db_response = vector_search(query)

    source_material = ""
    for doc in db_response['matches']:
        source_material += f"Content: {doc['metadata']['text']}"

    new_source_material = {
        "role": "assistant",
        "content": source_material,
    }

    conversation.append(new_source_material)

    llm_response = generate_response(conversation)

    return jsonify(llm_response)


if __name__ == '__main__':
    app.run(debug=True, port=5003)
