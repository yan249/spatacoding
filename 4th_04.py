from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.


## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index_02.html')

## API 역할을 하는 부분
@app.route('/reviews', methods=['POST'])
def write_review():
    print(request.form)
    name_receive = request.form['name']
    count_receive = request.form['count']
    ad_receive = request.form['address']
    phone_receive = request.form['phone']
	# 2. DB에 정보 삽입하기
    review = {
        'name': name_receive,
        'count': count_receive,
        'address': ad_receive,
        'phone': phone_receive
    }
    db.order.insert_one(review)
	# 3. 성공 여부 & 성공 메시지 반환하기
    return jsonify({'result': 'success', 'msg': '주문이 성공적으로 되었습니다.'})

@app.route('/reviews', methods=['GET'])
def read_reviews():
    send_data =[]
    book_order=list(db.order.find())
    print(book_order)
    for order in book_order:
        send_data.append({
            'name': order['name'],
            'count': order['count'],
            'address': order['address'],
            'phone': order['phone']
        })

    return jsonify({'result': 'success', 'data': send_data})


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)