from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


# API 역할을 하는 부분
@app.route('/api/list', methods=['GET'])
def show_stars():
    movie_star = list(db.mystar.find({}, {'_id': False}).sort("like", -1))
    return jsonify({'movie_stars': movie_star})


@app.route('/api/like', methods=['POST'])
def like_star():
    name_receive = request.form['name_give']
    target_star = db.mystar.find_one({'name': name_receive})
    current_like = target_star['like']
    db.mystar.update_one({'name': name_receive}, {'$set': {'like': current_like + 1}})
    return jsonify({'msg': name_receive + "님의 좋아요를 눌렀습니다."})


@app.route('/api/delete', methods=['POST'])
def delete_star():
    name_receive = request.form['name_give']
    db.mystar.delete_one({'name': name_receive})
    return jsonify({'msg': name_receive + "님을 삭제했습니다."})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
