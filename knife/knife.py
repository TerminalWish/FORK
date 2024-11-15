import os
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from urllib.parse import urljoin
from apscheduler.schedulers.background import BackgroundScheduler
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(os.path.join('instance', 'knife.db'))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

socketio = SocketIO(app, cors_allowed_origins="*")

SERVER_URL = 'http://localhost:5000'

### Cached Tables from Fork
class Menu(db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
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
    
class MenuIngredient(db.Model):
    __tablename__ = 'menu_ingredient'
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    quantity = db.Column(db.Float, nullable=False)
    measurement = db.Column(db.String, nullable=False)

    # Useful for debugging
    def __repr__(self):
        return f'<MenuIngredient {self.menu_id, self.ingredient_id}>'

# @app.route('/ingredients/<int:item_id>', methods=['GET'])
# def get_item_ingredients(item_id):
#     # Query MenuIngredient to get ingredient details, quantity, and measurement
#     # Also join with Ingredient to get the ingredient by name
#     menu_ingredients = (
#         db.session.query(MenuIngredient, Ingredient)
#         .join(Ingredient, MenuIngredient.ingredient_id == Ingredient.id)
#         .filter(MenuIngredient.menu_id == item_id)
#         .all()
#     )

#     # Step 2: Format the data to include all required fields
#     ingredient_data = [
#         {
#             "id": ingredient.id,
#             "name": ingredient.name,
#             "quantity": menu_ingredient.quantity,
#             "measurement": menu_ingredient.measurement
#         }
#         for menu_ingredient, ingredient in menu_ingredients
#     ]
    
#     return jsonify(ingredient_data)

# Route for Fork to notify Knife of an update
@app.route('/order/update', methods=['POST'])
def order_update():
    data = request.json  # Expecting Fork to send minimal data like `table_num`
    if not data or 'table_num' not in data:
        return jsonify({'error': 'Invalid update data'}), 400

    # Query Fork for updated Order information (e.g., all orders for the given table)
    try:
        table_num = data['table_num']
        get_order_url = urljoin(SERVER_URL, '/orders/get')
        response = requests.get(get_order_url, params={"table_num": table_num}, timeout=5)
        response.raise_for_status()  # Check if the request was successful
        order_data = response.json()

        # Enrich order data with menu item names from the cache
        for order in order_data:
            menu_item = Menu.query.filter_by(id=order['item_id']).first()
            side_item = Menu.query.filter_by(id=order['side_option_id']).first()
            if menu_item:
                order['item_name'] = menu_item.name

                # Get ingredients for this item from the MenuIngredient and Ingredient tables
                menu_ingredients = (
                    db.session.query(MenuIngredient, Ingredient)
                    .join(Ingredient, MenuIngredient.ingredient_id == Ingredient.id)
                    .filter(MenuIngredient.menu_id == order['item_id'])
                    .all()
                )

                # Attach ingredient details
                order['ingredients'] = [
                    {
                        "id": ingredient.id,
                        "name": ingredient.name,
                        "quantity": menu_ingredient.quantity,
                        "measurement": menu_ingredient.measurement
                    } for menu_ingredient, ingredient in menu_ingredients
                ]
            else:
                order['item_name'] = 'Unknown Item'  # Fallback if item is not found in cache
            
            if side_item:
                order['side_name'] = side_item.name
        
        # Broadcast the updated order data to all connected clientspyth
        socketio.emit('order_update', order_data)
        return jsonify({'status': 'Update received and broadcasted'}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve or broadcast order data', 'details': str(e)}), 500
    
@socketio.on('connect')
def handle_connect():
    print("Client connected")

def fetch_and_cache_data():
    # URLs for Fork's data endpoints
    menu_url = urljoin(SERVER_URL, '/menu_data')
    ingredient_url = urljoin(SERVER_URL, '/ingredient_data')
    menu_ingredient_url = urljoin(SERVER_URL, '/menu_ingredient_data')

    try:
        # Fetch Menu data
        menu_response = requests.get(menu_url)
        menu_data = menu_response.json()
        
        # Fetch Ingredient data
        ingredient_response = requests.get(ingredient_url)
        ingredient_data = ingredient_response.json()

        # Fetch MenuIngredient data
        menu_ingredient_response = requests.get(menu_ingredient_url)
        menu_ingredient_data = menu_ingredient_response.json()

        with app.app_context():
            # Clear existing cached data
            Menu.query.delete()
            Ingredient.query.delete()
            MenuIngredient.query.delete()

            # Insert Menu data
            for item in menu_data:
                new_menu = Menu(
                    id=item['id'],
                    name=item['name'],
                    category=item['category'],
                    availability=item['availability']
                )
                db.session.add(new_menu)

            # Insert Ingredient data
            for item in ingredient_data:
                new_ingredient = Ingredient(
                    id=item['id'],
                    name=item['name']
                )
                db.session.add(new_ingredient)

            # Insert MenuIngredient data
            for item in menu_ingredient_data:
                new_menu_ingredient = MenuIngredient(
                    menu_id=item['menu_id'],
                    ingredient_id=item['ingredient_id'],
                    quantity=item['quantity'],
                    measurement=item['measurement']
                )
                db.session.add(new_menu_ingredient)

            # Commit all changes to the database
            db.session.commit()
            
            print("Cache tables updated successfully.")

    except Exception as e:
        print("Error fetching or caching data:", e)

def start_cache_scheduler():
    # Run the initial cache update immediately
    fetch_and_cache_data()
    
    # Set up the scheduler to update every 15 minutes thereafter
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_cache_data, 'interval', minutes=15)
    scheduler.start()

if __name__ == '__main__':

    # Start the initial cache update and scheduler
    start_cache_scheduler()
    
    # Run the socket server
    socketio.run(app, debug=True, host='0.0.0.0', port=5002)
