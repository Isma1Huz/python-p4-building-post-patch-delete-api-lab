#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    name = data.get('name')
    price = data.get('price')

    if name is None or price is None:
        return jsonify(error='Both name and price are required'), 400

    new_baked_good = BakedGood(name=name, price=price)
    db.session.add(new_baked_good)
    db.session.commit()

    baked_good_data = {
        "id": new_baked_good.id,
        "name": new_baked_good.name,
        "price": new_baked_good.price,
        "created_at": new_baked_good.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
        "updated_at": new_baked_good.updated_at.strftime("%Y-%m-%dT%H:%M:%S")
    }

    return jsonify(baked_good_data), 201




@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get(id)

    if bakery is None:
        return jsonify(error='Bakery not found'), 404

    data = request.form
    new_name = data.get('name')

    if new_name:
        bakery.name = new_name
        db.session.commit()

        bakery_data = {
            "id": bakery.id,
            "name": bakery.name,
            "created_at": bakery.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
            "updated_at": bakery.updated_at.strftime("%Y-%m-%dT%H:%M:%S")
        }

        return jsonify(bakery_data), 200
    else:
        return jsonify(error='No data provided for update'), 400




@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)

    if baked_good:
        db.session.delete(baked_good)
        db.session.commit()
        return jsonify(message='Baked good successfully deleted'), 200
    else:
        return jsonify(error='Baked good not found'), 404


if __name__ == '__main__':
    app.run(port=5555, debug=True)
