from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbhomework


def phone_number_check(phone_number):
    if len(phone_number) != 13:
        return False
    if phone_number[3] != '-' or phone_number[8] != '-':
        return False
    return True


## HTML 화면 보여주기
@app.route('/')
def homework():
    return render_template('index.html')


# 주문하기(POST) API
@app.route('/order', methods=['POST'])
def save_order():
    name_receive = request.form['name_give']
    address_receive = request.form['address_give']
    count_receive = request.form['count_give']
    phone_receive = request.form['phone_give']

    if name_receive == "":
        return jsonify({'msg': '이름을 입력하세요.'})
    if address_receive == "":
        return jsonify({'msg': '주소를 입력하세요.'})
    if count_receive == '-- 수량을 선택하세요 --':
        return jsonify({'msg': '수량을 선택하세요.'})
    if phone_receive == "":
        return jsonify({'msg': '전화번호를 입력하세요.'})
    if not phone_number_check(phone_receive):
        return jsonify({'msg': '휴대폰 입력 형식이 틀립니다.\n***-****-**** 형태로 입력해주세요.'})

    doc = {
        'name': name_receive,
        'address': address_receive,
        'count': count_receive,
        'phone': phone_receive
    }

    db.shopping.insert_one(doc)

    return jsonify({'msg': '주문되었습니다.'})


# 주문 목록보기(Read) API
@app.route('/order', methods=['GET'])
def view_orders():
    customers = list(db.shopping.find({}, {'_id': False}))
    return jsonify({'all_customers': customers})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
