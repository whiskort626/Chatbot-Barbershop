from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def root():
    return "root"
'''
GET 
POST
PUT
DELETE
'''

@app.route('/users/<user_id>')
def get_user(user_id):
    user_data = {
        "user_id": user_id,
        "name": "John Doe",
        "email": "john.doe@example.com"
    }
    # /users/2654?query=query_test
    query = request.args.get('query')
    if query:
        user_data['query'] = query
    return jsonify(user_data), 200

@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.get_json()
    user_data['status'] = 'success'
    return jsonify(user_data), 201

if __name__ == "__main__":
    app.run(debug=True)

