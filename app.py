from flask import Flask, jsonify, request
# from Model import vector_search
from llm import generate_response

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def predict():
    req = request.json
    query = req["query"]
    conversation = req["conversation"]
    chat_history_no = req["chat_history_no"]
    # db_response = vector_search(query)
    source_material = ""
    # for doc in db_response:
    #     source_material += f"Title: {doc['title']}, Content: {doc['content']}, Url: {doc['url']}\n"
    
    new_source_material = {
        "role": "assistant",
        "content": source_material,
    }

    conversation.append(new_source_material)

    llm_response = generate_response(conversation)
    

    return jsonify(llm_response)

if __name__ == '__main__':
    app.run(debug=True)