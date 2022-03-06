import json

import pymongo as pymongo
from bson import ObjectId
from flask import Flask, request

app = Flask(__name__)

client = pymongo.MongoClient(
    "mongodb+srv://admin:z6HFhyO952qVJvAT@cluster0.ay330.mongodb.net/word_tier_list?retryWrites=true&w=majority")
db = client.words

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@app.route('/')
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
    return 'Word deleted successfully'

def add_word():
    # get the data from the request
    data = request.get_json()
    # insert the data into the database
    db.words.insert_one(data)
    return 'Word added successfully'

def get_all_words():
    # get all the words from the database
    words = db.words.find()
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
    return 'Word deleted successfully'

def update_word():
    # get the data from the request
    data = request.get_json()
    # update the word in the database
    data['_id'] = ObjectId(data['_id'])
    query = {"_id": data['_id']}
    new_values = {"$set": {'_id': data['_id'], 'word': data['word'], 'tier': data['tier'], 'definition': data['definition']}}
    db.words.update_one(query, new_values)
    return 'Word updated successfully'

if __name__ == '__main__':
    app.run()
