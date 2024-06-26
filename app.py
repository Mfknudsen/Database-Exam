import os
from flask import Flask, jsonify, request
from Model import vector_search, generate_response

app = Flask(__name__)


@app.route('/chat', methods=['POST'])
def predict():
    req = request.json
    query = req["query"]
    conversation = req["conversation"]

    db_response = vector_search(query)

    topic = "Off topic"
    source_material = ""
    if 'matches' in db_response and len(db_response['matches']) > 0:
        topic = db_response['matches'][0]['metadata']['title']
        for doc in db_response['matches']:
            source_material += f"Content: {doc['metadata']['text']}\n"

    new_source_material = {
        "role": "assistant",
        "content": source_material,
    }

    conversation.append(new_source_material)

    llm_response = generate_response(conversation)

    response = {
        "llm_response": llm_response,
        "topic": topic
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, port=5003)
