import json
import os

import pymongo as pymongo
from bson import ObjectId
from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

client = pymongo.MongoClient("mongodb+srv://admin:z6HFhyO952qVJvAT@cluster0.ay330.mongodb.net/word_tier_list?retryWrites=true&w=majority")
db = client.words

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@app.route('/')
@cross_origin()
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/words', methods=['GET', 'POST', 'DELETE', 'PUT'])
def manage_word():
    if request.method == 'POST':
        return add_word()
    elif request.method == 'GET':
        return get_all_words()
    elif request.method == 'DELETE':
        return delete_word()
    elif request.method == 'PUT':
        return update_word()

@app.route('/words/<id>', methods=['GET', 'DELETE'])
def manage_word_by_id(id):
    id = ObjectId(id)
    if request.method == 'GET':
        return get_word_by_id(id)
    elif request.method == 'DELETE':
        return delete_word_by_id(id)

def get_word_by_id(id):
    # get the word from the database
    word = db.words.find_one({'_id': id})
    word = JSONEncoder().encode(word)
    # convert the word to a json string
    return str(word)

def delete_word_by_id(id):
    # delete the word from the database
    db.words.delete_one({'_id': id})
    response = app.response_class(
        response=json.dumps({'message': 'Word deleted successfully'}),
        status=200,
        mimetype='application/json'
    )
    return response

def add_word():
    # get the data from the request
    data = request.get_json()
    # insert the data into the database
    db.words.insert_one(data)
    data = JSONEncoder().encode(data)
    response = app.response_class(
        response=json.dumps({'message': 'Word added successfully', 'data': data}),
        status=200,
        mimetype='application/json'
    )
    return response

def get_all_words():
    # get all the words from the database sorted by tier
    words = db.words.find().sort('tier', pymongo.DESCENDING)
    # convert the words to a list
    words_list = [word for word in words]
    words_list = JSONEncoder().encode(words_list)
    # convert the list to a json string
    return str(words_list)

def delete_word():
    # get the data from the request
    data = request.get_json()
    # delete the word from the database
    db.words.delete_one(data)
    data = JSONEncoder().encode(data)
    response = app.response_class(
        response=json.dumps({'message': 'Word deleted successfully', 'data': data}),
        status=200,
        mimetype='application/json'
    )
    return response

def update_word():
    # get the data from the request
    data = request.get_json()
    # data = JSONEncoder().encode(data)
    word = data['word']
    # update the word in the database
    query = {"_id": ObjectId(word['_id'])}
    new_values = {"$set": {'name': word['name'], 'tier': word['tier'], 'definition': word['definition']}}
    db.words.update_one(query, new_values)
    response = app.response_class(
        response=json.dumps({'message': 'Word updated successfully', 'data': data}),
        status=200,
        mimetype='application/json'
    )
    return response
