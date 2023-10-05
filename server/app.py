#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route("/")
def index():
    return "<h1>Bakery GET API</h1>"

@app.route("/bakeries")
def bakeries():
    bakery_list = Bakery.query.all()
    bakery_list_dict = [bakery.to_dict() for bakery in bakery_list]
    json_data = jsonify(bakery_list_dict)
    return make_response(json_data, 200)

@app.route("/bakeries/<int:id>")
def bakery_by_id(id):
    # bakery = Bakery.query.get(id)
    # session = db.session
    bakery = db.session.get(Bakery, id)

    if bakery is None:
        return make_response({"error": "Bakery not not found"}, 404)
    
    bakery_dict = bakery.to_dict()
    json_data = jsonify(bakery_dict)

    return json_data

@app.route("/baked_goods/by_price")
def baked_goods_by_price():
    goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    if goods is None:
        return make_response({"error": "No baked goods found"}, 404)
    goods_dict = [good.to_dict() for good in goods]
    json_data = jsonify(goods_dict)

    return make_response(json_data, 200)

@app.route("/baked_goods/most_expensive")
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive is None:
        return make_response({"error": "No baked goods found"}, 404)
    
    most_expensive_dict = most_expensive.to_dict()
    json_data = jsonify(most_expensive_dict)

    return make_response(json_data, 200)

if __name__ == "__main__":
    app.run(port=5555, debug=True)
