#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    resp_list = []
    for bakery in Bakery.query.all():
        bak_dict = bakery.to_dict()
        resp_list.append(bak_dict)
    
    response = make_response(jsonify(resp_list), 200, {"Content-Type": "application/json"})

    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bak_found = Bakery.query.filter(id == Bakery.id).first()
    bake_dict = bak_found.to_dict()
    response = make_response(jsonify(bake_dict), 200)
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    dict_list = []
    baked_goods_sorted = BakedGood.query.order_by(BakedGood.price).all()
    for baked in baked_goods_sorted:
        b_dict = baked.to_dict()
        dict_list.append(b_dict)
    
    response = make_response(dict_list, 200)
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(db.desc(BakedGood.price)).first()
    resp_dict = most_expensive.to_dict()

    response = make_response(resp_dict, 200)
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
