import os
import json
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
    item_category = db.Column(db.String, nullable=False)
    side_option_id = db.Column(db.Integer, nullable=True)
    side_option_name = db.Column(db.String, nullable=True)
    mods = db.Column(db.Text, default='[]')
    side_mods = db.Column(db.Text, default='[]')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            'seat_number': self.seat_number,
            'item_id': self.item_id,
            'item_name': self.item_name
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
    item_category = data['item_category']

    # Create and add a new TempOrder instance
    new_order = TempOrder(
        table_num=table_num,
        seat_number=seat_number,
        item_id=item_id,
        item_name=item_name,
        item_category=item_category
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
        entree.side_mods = json.dumps([])
        db.session.commit()
        return jsonify({'message': 'Side added to entree successfully'})
    
    return jsonify({'message': 'Entree not found'}), 404

@app.route('/order/intensity_mod', methods=['POST'])
def intensity_mod():
    data = request.json
    table_num = data['table_num']
    seat_number = data['seat_number']
    intensity = data['intensity']
    ingredient = data['ingredient']

    dish = TempOrder.query.filter_by(seat_number=seat_number, table_num=table_num).first()
    if not dish:
        return jsonify({'error': 'Order item not found'}), 404

    current_mods = json.loads(dish.mods)
    if not current_mods:
        current_mods = []
    current_mods.append({
        'intensity': intensity,
        'ingredient': ingredient
    })

    dish.mods = json.dumps(current_mods)
    db.session.commit()

    return jsonify({'message': 'Mod added to item', 'mods': current_mods}), 200

@app.route('/order/side_intensity_mod', methods=['POST'])
def side_intensity_mod():
    data = request.json
    table_num = data['table_num']
    seat_number = data['seat_number']
    intensity = data['intensity']
    ingredient = data['ingredient']

    dish = TempOrder.query.filter_by(seat_number=seat_number, table_num=table_num).first()
    if not dish:
        return jsonify({'error': 'Order item not found'}), 404
    
    current_side_mods = json.loads(dish.side_mods) if dish.side_mods else []
    current_side_mods.append({
        'intensity': intensity,
        'ingredient': ingredient
    })

    dish.side_mods = json.dumps(current_side_mods)
    db.session.commit()

    return jsonify({'message': 'Side mod added to item', 'mods': current_side_mods}), 200

@app.route('/order/remove_mod', methods=['POST'])
def remove_mod():
    data = request.json
    seat_number = data.get('seat_number')
    item_id = data.get('item_id')
    ingredient = data.get('ingredient')

    # Retrieve the order item based on seat_number and item_id
    dish = TempOrder.query.filter_by(seat_number=seat_number, item_id=item_id).first()
    if not dish:
        return jsonify({'error': 'Order item not found'}), 404
    
    # Parse and update the mods list
    current_mods = json.loads(dish.mods) if dish.mods else []
    updated_mods = [mod for mod in current_mods if mod['ingredient'] != ingredient]

    # Save the updated mods back to the database
    dish.mods = json.dumps(updated_mods)
    db.session.commit()

    return jsonify({'success': True, 'mods': updated_mods}), 200

@app.route('/order/side_remove_mod', methods=['POST'])
def side_remove_mod():
    data = request.json
    seat_number = data.get('seat_number')
    entree_item_id = data.get('item_id') # Remember this is stored under the entree id as a side
    ingredient = data.get('ingredient')

    # Retrieve the order item based on seat_number and item_id
    dish = TempOrder.query.filter_by(seat_number=seat_number, item_id=entree_item_id).first()
    if not dish:
        return jsonify({'error': 'Order item not found'}), 404
    
    # Parse and update the mods list
    current_mods = json.loads(dish.side_mods) if dish.side_mods else []
    updated_mods = [mod for mod in current_mods if mod['ingredient'] != ingredient]

    dish.side_mods = json.dumps(updated_mods)
    db.session.commit()

    return jsonify({'success': True, 'mods': updated_mods}), 200


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

    return jsonify({'message': 'Mod added to item'}), 200

@app.route('/order/finalize', methods=['POST'])
def finalize_order():
    table_num = request.json.get('table_num')

    # Retrieve all items for the given table number
    orders = TempOrder.query.filter_by(table_num=table_num).all()
    final_order = []

    for order in orders:
        item_data = {
            'table_num': table_num,
            'item_id': order.item_id,
            'side_option_id': order.side_option_id,
            'mods': json.loads(order.mods) if order.mods else [],
            'side_mods': json.loads(order.side_mods) if order.side_mods else []
        }
        final_order.append(item_data)

    # Send final_order to Fork for permanence
    try:
        place_order_url = urljoin(SERVER_URL, '/orders/place')
        response = requests.post(place_order_url, json={'orders': final_order}, timeout=5)
        
        # Clear all entries for this table from TempOrder after finalizing
        TempOrder.query.filter_by(table_num=table_num).delete()
        db.session.commit()
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({'error': 'Failed to send order to Fork', 'details': str(e)}), 500
    
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
                'side_option_name': order.side_option_name,
                'seat_number': order.seat_number,
                'item_category': order.item_category
            }
        if order.mods:
            # Parse the JSON string into a list of mod dictionaries
            mods_list = json.loads(order.mods)

            # Append each mod to the order dictionary under 'mods'
            for mod in mods_list:
                order_dict[order.seat_number]['mods'].append(mod)

    return jsonify({'order': order_dict})

@app.route('/get_ingredients/<dish_id>', methods=['GET'])
def get_ingredients_by_dish(dish_id):
    if not dish_id:
        return jsonify({"error": "Dish ID is required", "error_code": "MISSING_DISH_ID"}), 400

    try:
        # Request ingredients from Fork
        ingredients_url = urljoin(SERVER_URL, '/dish/ingredients')
        response = requests.get(ingredients_url, params={"dish_id": dish_id}, timeout=5)
        response.raise_for_status()
        ingredients_data = response.json()
        
        # Check if response contains error
        if not ingredients_data.get("success", False):
            return jsonify(ingredients_data), response.status_code
        
        return jsonify(ingredients_data), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to retrieve ingredients", "error_code": e}), 500

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
    
@app.route('/order/get_mods', methods=['POST'])
def get_mods():
    data = request.json
    seat_number = data.get('seat_number')
    item_id = data.get('item_id')

    # Retrieve the order item based on seat_number and item_id
    dish = TempOrder.query.filter_by(seat_number=seat_number, item_id=item_id).first()
    if not dish:
        return jsonify({'error': 'Order item not found'}), 404

    # Parse the mods field, assuming it's stored as JSON in the database
    current_mods = json.loads(dish.mods) if dish.mods else []

    # Return the current mods
    return jsonify({'mods': current_mods}), 200

@app.route('/order/get_side_mods', methods=['POST'])
def get_side_mods():
    data = request.json
    seat_number = data.get('seat_number')
    entree_item_id = data.get('item_id')  # The main entree's ID to locate the side's mods

    # Find the entree with the given seat_number and entree_item_id
    dish = TempOrder.query.filter_by(seat_number=seat_number, item_id=entree_item_id).first()
    if not dish:
        return jsonify({'error': 'Order item not found'}), 404

    # Parse side_mods (stored as JSON) if available, otherwise return an empty list
    side_mods = json.loads(dish.side_mods) if dish.side_mods else []

    return jsonify({'mods': side_mods}), 200 

if __name__ == '__main__':
    app.run(debug=True, port=5001)
