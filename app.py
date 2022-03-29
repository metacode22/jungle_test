from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from bson.json_util import dumps
from bson.objectid import ObjectId

from pymongo import MongoClient
client = MongoClient('mongodb://test:test@13.125.205.52',27017)
db = client.dbjungle

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/show', methods=['GET'])
def show_memo():
    result = list(db.memos.find({}))

    return jsonify({'result': 'success', 'memos': dumps(result)})

@app.route('/api/post', methods=['POST'])
def post_memo():
    title_receive = request.form['title_give']
    comment_receive = request.form['comment_give']
    memo = {'title': title_receive, 'comment': comment_receive}

    db.memos.insert_one(memo)

    return jsonify({'result': 'success'})

@app.route('/api/update', methods=['POST'])
def update_memo():
    new_title_receive = request.form['new_title_give']
    new_text_receive = request.form['new_text_give']
    _id_receive = request.form['_id_give']

    db.memos.update_one({'_id' : ObjectId(_id_receive)}, {'$set':{'title': new_title_receive}})
    db.memos.update_one({'_id' : ObjectId(_id_receive)}, {'$set':{'comment': new_text_receive}})

    return jsonify({'result': 'success'})

@app.route('/api/delete', methods=['POST'])
def delete_memo():
    _id_receive = request.form['_id_give']

    db.memos.delete_one({'_id' : ObjectId(_id_receive)})

    return jsonify({'result': 'success'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)