#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from sqlalchemy import desc

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
    
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]

    response = make_response(bakeries, 200)

    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()

    bakery_dict = bakery.to_dict()

    response = make_response(bakery_dict, 200)

    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    price = request.args.get('price', type=float)
    if price is not None:
        baked_goods = BakedGood.query.filter(BakedGood.price >= price).order_by(desc(BakedGood.price)).all()
    else:
        baked_goods = BakedGood.query.order_by(desc(BakedGood.price)).all()
    baked_goods_list = []
    for good in baked_goods:
        bakery_dict = None
        if good.bakery:
            bakery_dict = {
                'id': good.bakery.id,
                'name': good.bakery.name,
                'created_at': str(good.bakery.created_at),
                'updated_at': str(good.bakery.updated_at) if good.bakery.updated_at else None
            }
            
        baked_good_dict = {
                'id': good.id,
                'name': good.name,
                'price': good.price,
                'created_at': str(good.created_at),
                'updated_at': str(good.updated_at) if good.updated_at else None,
                'bakery_id': good.bakery_id,
                'bakery': bakery_dict
            }
            
        baked_goods_list.append(baked_good_dict)
    response = make_response(jsonify(baked_goods_list), 200)
    return response
    
        
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_baked_good = db.session.query(BakedGood) \
        .filter(BakedGood.price != None) \
        .order_by(BakedGood.price.desc()) \
        .first()
        
    if most_expensive_baked_good:
        bakery_data = None
        if most_expensive_baked_good.bakery:
            bakery_data = {
                'id': most_expensive_baked_good.bakery.id,
                'name': most_expensive_baked_good.bakery.name,
                'created_at': str(most_expensive_baked_good.bakery.created_at),
                'updated_at': str(most_expensive_baked_good.bakery.updated_at) if most_expensive_baked_good.bakery.updated_at else None
                }
            
        response_data = {
            'id': most_expensive_baked_good.id,
            'name': most_expensive_baked_good.name,
            'price': most_expensive_baked_good.price,
            'created_at': str(most_expensive_baked_good.created_at),
            'updated_at': str(most_expensive_baked_good.updated_at) if most_expensive_baked_good.updated_at else None,
            'bakery_id': most_expensive_baked_good.bakery_id,
            'bakery': bakery_data
            }

        return jsonify(response_data), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
