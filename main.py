#!flask/bin/python

from flask import request
from flask import Flask, jsonify, abort
import redis
app = Flask(__name__)
r_server = redis.Redis("localhost")

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    print task
    r_server.set("1", task)
    return jsonify({'task': task}), 201

if __name__ == '__main__':
    print(r_server.get("name"))
    print(r_server.get("1"))
    app.run(debug=True)

