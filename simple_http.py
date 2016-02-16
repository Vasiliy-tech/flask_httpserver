from flask import Flask, abort, request
import json
from time import strftime
from storage import data

DELETE_STATUS = 'null'
REQUEST_KEY = 'key'
REQUEST_VALUE = 'value'

app = Flask(__name__)


def create_response(result):
    res = {}
    res['result'] = result
    res['time'] = strftime("%Y-%m-%d %H:%M")
    response = json.dumps(res, encoding='utf-8')
    return response

@app.route('/')
def hello_world():
    return json.dumps(data)


@app.route('/dictionary', methods=['POST'])
def dictionary_index():
    req = request.get_data()
    req_dict = {}

    try:
        req_dict = json.loads(req, 'utf-8')
    except ValueError:
        abort(400)

    new_key = req_dict.get(REQUEST_KEY)
    new_value = req_dict.get(REQUEST_VALUE)

    if new_value == None or new_key == None:
        abort(400)

    if data.get(new_key) == None:
        data.update({new_key: new_value})
    else:
        abort(409)

    response = create_response(new_value)
    return response


@app.route('/dictionary/<key>', methods=['PUT'])
def dictionary_put(key):
    req = request.get_data()
    req_dict = {}
    try:
        req_dict = json.loads(req, 'utf-8')
    except ValueError:
        abort(400)

    new_value = req_dict.get(REQUEST_VALUE)
    if new_value == None:
        abort(400)

    if data.get(key) != None:
        data.update({key: new_value})
    else:
        abort(404)

    response = create_response(new_value)
    return response


@app.route('/dictionary/<key>', methods=['GET'])
def dictionary_get(key):
    result = data.get(key)
    if result == None:
        abort(404)
    response = create_response(result)
    return response


@app.route('/dictionary/<key>', methods=['DELETE'])
def function_delete(key):
    try:
        data.pop(key)
    except KeyError:
        pass
    response = create_response(DELETE_STATUS)
    return response



if __name__ == '__main__':
    # app.debug = True
    app.run()

