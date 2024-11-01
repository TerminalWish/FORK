import os
from datetime import datetime
from urllib.parse import urljoin
from flask import Flask, render_template, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_migrate import Migrate

import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(os.path.join('instance', 'spoon.db'))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

SERVER_URL = 'http://localhost:5000'

# Initialize SQLAlchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Set up the engine and scoped session
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"], echo=True)
Session = scoped_session(sessionmaker(bind=engine))

class TempOrder(db.Model):
    __tablename__ = 'temp_orders'

    id = db.Column(db.Integer, primary_key=True)
    table_num = db.Column(db.Integer, nullable=False)
    seat_number = db.Column(db.Integer, nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    item_name = db.Column(db.String, nullable=False)
    side_option_id = db.Column(db.Integer, nullable=True)
    side_option_name = db.Column(db.String, nullable=True)
    mod_name = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            'seat_number': self.seat_number,
            'item_id': self.item_id,
            'item_name': self.item_name,
            'mod_name': self.mod_name
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/order/add_item', methods=['POST'])
def add_item():
    data = request.json
    table_num = data['table_num']
    seat_number = data['seat_number']
    item_id = data['item_id']
    item_name = data['item_name']
    
    # Create and add a new TempOrder instance
    new_order = TempOrder(
        table_num=table_num,
        seat_number=seat_number,
        item_id=item_id,
        item_name=item_name
    )
    db.session.add(new_order)
    db.session.commit()
    
    return jsonify({'message': 'Item added to order'})

@app.route('/order/add_side_to_entree', methods=['POST'])
def add_side_to_entree():
    data = request.json
    table_num = data['table_num']
    seat_number = data['seat_number']
    side_id = data['side_id']
    side_name = data['side_name']

    entree = TempOrder.query.filter_by(seat_number=seat_number, table_num=table_num).first()

    if entree:
        entree.side_option_id = side_id
        entree.side_option_name = side_name
        db.session.commit()
        return jsonify({'message': 'Side added to entree successfully'})
    
    return jsonify({'message': 'Entree not found'}), 404

@app.route('/order/add_mod', methods=['POST'])
def add_mod_to_item():
    data = request.json
    table_num = data['table_num']
    seat_number = data['seat_number']
    mod_name = data['mod_name']
    mod_id = data['mod_id']

    # Create a new TempOrder entry specifically for the modification
    new_mod = TempOrder(
        table_num=table_num,
        seat_number=seat_number,
        item_id=mod_id,
        item_name='',  # Optional: leave empty or use a placeholder for mods
        mod_name=mod_name
    )
    db.session.add(new_mod)
    db.session.commit()

    return jsonify({'message': 'Mod added to item'})

@app.route('/order/finalize', methods=['POST'])
def finalize_order():
    table_num = request.json.get('table_num')
    
    # Retrieve all items for the given table number
    orders = TempOrder.query.filter_by(table_num=table_num).all()
    final_order = {}
    
    for order in orders:
        if order.seat_number not in final_order:
            final_order[order.seat_number] = {
                'item_id': order.item_id,
                'item_name': order.item_name,
                'mods': []
            }
        if order.mod_name:
            final_order[order.seat_number]['mods'].append(order.mod_name)
    
    # Delete all entries for the table number after finalizing
    TempOrder.query.filter_by(table_num=table_num).delete()
    db.session.commit()
    
    # TODO: Send `final_order` to FORK for permanent storage (implement as needed)
    
    return jsonify({'message': f'Order for table {table_num} finalized', 'final_order': final_order})

    
@app.route('/order/get', methods=['GET'])
def get_current_order():
    table_num = request.args.get('table_num')
    
    # Query all items for the given table number
    orders = TempOrder.query.filter_by(table_num=table_num).all()
    
    order_dict = {}
    for order in orders:
        if order.seat_number not in order_dict:
            order_dict[order.seat_number] = {
                'item_id': order.item_id,
                'item_name': order.item_name,
                'mods': [],
                'side_option_id': order.side_option_id,
                'side_option_name': order.side_option_name
            }
        if order.mod_name:
            order_dict[order.seat_number]['mods'].append(order.mod_name)

    return jsonify({'order': order_dict})

@app.route('/get_menu/<category>', methods=['GET'])
def get_menu_by_category(category):
    try:
        menu_url = urljoin(SERVER_URL, '/menu')
        response = requests.get(menu_url, timeout=5)
        response.raise_for_status()

        menu_list = response.json()

        if category.lower() != 'all':
            filter_list = [item for item in menu_list if item['category'].lower() == category.lower()]
            return jsonify(filter_list)

        # Return full menu if 'all'
        return jsonify(menu_list)

    except requests.Timeout:
        return jsonify({'erorr': 'Request timed out'}), 504
    except requests.RequestException as e:
        return jsonify({'error': f'Request failed: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)