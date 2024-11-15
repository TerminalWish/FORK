import os
import json
from flask import Flask, jsonify, request
from urllib.parse import urljoin
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import requests


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(os.path.join('instance', 'fork.db'))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
KNIFE_SERVER_URL = 'http://localhost:5002'

# Initialize SQLAlchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Set up the engine and scoped session
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"], echo=True)
Session = scoped_session(sessionmaker(bind=engine))

### Base Tables
class Menu(db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String, nullable=False)
    availability = db.Column(db.Boolean, default=True)

    # Useful for debugging
    def __repr__(self):
        return f'<Menu {self.name}>'

class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    menu = relationship('Menu', secondary='menu_ingredient', backref='ingredient')

    # Useful for debugging
    def __repr__(self):
        return f'<Ingredient {self.name}>'
    
class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    side_option_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=True)
    table_num = db.Column(db.Integer, nullable=False)
    mods = db.Column(db.Text, default='[]')
    side_mods = db.Column(db.Text, default='[]')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())
    status = db.Column(db.String, nullable=False, default='new')

    # Relationships
    item = relationship("Menu", foreign_keys=[item_id])
    side_option = relationship("Menu", foreign_keys=[side_option_id])

    def to_dict(self):
        return {
            'seat_number': self.seat_number,
            'item_id': self.item_id
        }

### Relationship Tables
class MenuIngredient(db.Model):
    __tablename__ = 'menu_ingredient'
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    quantity = db.Column(db.Float, nullable=False)
    measurement = db.Column(db.String, nullable=False)

    # Useful for debugging
    def __repr__(self):
        return f'<MenuIngredient {self.menu_id, self.ingredient_id}>'

### Cache building routes
@app.route('/menu_data', methods=['GET'])
def menu_data_cache():
    menu_items = Menu.query.all()
    menu_data = [
        {
            'id': item.id,
            'name': item.name,
            'category': item.category,
            'availability': item.availability
        } for item in menu_items
    ]
    return jsonify(menu_data)

@app.route('/ingredient_data', methods=['GET'])
def ingredient_data_cache():
    ingredient_items = Ingredient.query.all()
    ingredient_data = [
        {
            'id': item.id,
            'name': item.name
        } for item in ingredient_items
    ]
    return jsonify(ingredient_data)

@app.route('/menu_ingredient_data', methods=['GET'])
def menu_ingredient_data_cache():
    menu_ingredient_items = MenuIngredient.query.all()
    menu_ingredient_data = [
        {
            'menu_id': item.menu_id,
            'ingredient_id': item.ingredient_id,
            'quantity': item.quantity,
            'measurement': item.measurement
        } for item in menu_ingredient_items
    ]
    return jsonify(menu_ingredient_data)

### Routing Methods
@app.route('/menu', methods=['GET'])
def get_menu():
    session = Session()

    menu_items = session.query(Menu).all()
    menu_list = [item.as_dict() for item in menu_items]

    session.close()

    return jsonify(menu_list)

@app.route('/orders/get', methods=['GET'])
def get_order_by_table():
    table_num = request.args.get('table_num')
    if table_num is None:
        return jsonify({'error': 'Table number is required'}), 400
    
    # Query orders for the specified table
    orders = Order.query.filter_by(table_num=table_num).all()

    # Convert orders to a serializable format
    order_data = [{
        'id': order.id,
        'table_num': order.table_num,
        'item_id': order.item_id,
        'side_option_id': order.side_option_id,
        'mods': order.mods,
        'side_mods': order.side_mods,
        'status': order.status,
        'created_at': order.created_at,
        'updated_at': order.updated_at
    } for order in orders]

    return jsonify(order_data), 200

@app.route('/dish/ingredients', methods=['GET'])
def get_ingredients():
    dish_id = request.args.get('dish_id')
    if not dish_id:
        return jsonify({"error": "Dish ID is required", "error_code": "MISSING_DISH_ID"}), 400

    try:
        # Query for ingredients associated with the specified menu item
        ingredients = (
            db.session.query(Ingredient.id, Ingredient.name, MenuIngredient.quantity, MenuIngredient.measurement)
            .join(MenuIngredient, Ingredient.id == MenuIngredient.ingredient_id)
            .filter(MenuIngredient.menu_id == dish_id)
            .all()
        )

        # Format response data
        ingredients_data = [
            {
                "id": ing.id,
                "name": ing.name,
                "quantity": ing.quantity,
                "measurement": ing.measurement
            }
            for ing in ingredients
        ]

        return jsonify({"success": True, "ingredients": ingredients_data}), 200
    
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "error_code": e}), 500

@app.route('/orders/place', methods=['POST'])
def place_order():
    data = request.json
    orders = data.get('orders')

    if not orders:
        return jsonify({'error': 'Invalid order data'}), 400
    
    new_orders = []
    table_num = None  # Initialize table_num to check for consistency
    for order in orders:
        try:
            if table_num is None:
                table_num = order.get('table_num')
            elif table_num != order.get('table_num'):
                return jsonify({'error': 'Inconsistent table numbers in order data'}), 400

            an_order = Order(
                table_num=table_num,
                item_id=order.get('item_id'),
                side_option_id=order.get('side_option_id'),  # Fixing typo here
                mods=json.dumps(order.get('mods', [])),
                side_mods=json.dumps(order.get('side_mods', [])),
                status='new'
            )
            new_orders.append(an_order)
        except Exception as e:
            return jsonify({'error': f'Failed to process items: {str(e)}'}), 400

    try:
        db.session.bulk_save_objects(new_orders)
        db.session.commit()

        # Notify Knife of the update
        notify_knife_of_update(table_num)

    except Exception as e:
        db.session.rollback()
        print(f"Error details: {e}")
        return jsonify({'error': 'Failed to save orders to database', 'details': str(e)}), 500

    return jsonify({'message': f'Order for table {table_num} placed successfully', 'order_count': len(new_orders)}), 201


# Helper function to aid with jsonifying table data
def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

setattr(Menu, "as_dict", as_dict)

# Helper function to update Knife of order updates
def notify_knife_of_update(table_num):
    try:
        update_url = urljoin(KNIFE_SERVER_URL, '/order/update')
        response = requests.post(update_url, json={"table_num": table_num}, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to notify Knife of update: {e}")

# Teardown to remove the session after each request
@app.teardown_appcontext
def remove_session(exception=None):
    Session.remove() # Ensures all sessions are closed after request

if __name__ == "__main__":
    app.run(debug=True, port=5000)