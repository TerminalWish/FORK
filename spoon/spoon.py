from flask import Flask, render_template, jsonify
from urllib.parse import urljoin
import requests

app = Flask(__name__)

SERVER_URL = 'http://localhost:5000'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_menu')
def get_menu():
    try:
        menu_url = urljoin(SERVER_URL, '/menu')
        response = requests.get(menu_url, timeout=5)
        response.raise_for_status()
        menu_list = response.json()
        return jsonify(menu_list)
    except requests.Timeout:
        return {'error': 'Request timed out'}
    except requests.RequestException as e:
        return jsonify({'error': f'{e}'}), 500
    
@app.route('/get_menu/drink')
def get_drinks():
    try:
        menu_url = urljoin(SERVER_URL, '/menu')
        response = requests.get(menu_url, timeout=5)
        response.raise_for_status()
        menu_list = response.json()
        drink_list = [item for item in menu_list if item['category'] == 'Drink']
        return jsonify(drink_list)
    except requests.Timeout:
        return {'error': 'Request timed out'}
    except requests.RequestException as e:
        return jsonify({'error': f'{e}'}), 500
    
@app.route('/get_menu/appetizer')
def get_appetizers():
    try:
        menu_url = urljoin(SERVER_URL, '/menu')
        response = requests.get(menu_url, timeout=5)
        response.raise_for_status()
        menu_list = response.json()
        appetizer_list = [item for item in menu_list if item['category'] == 'Appetizer']
        return jsonify(appetizer_list)
    except requests.Timeout:
        return {'error': 'Request timed out'}
    except requests.RequestException as e:
        return jsonify({'error': f'{e}'}), 500

@app.route('/get_menu/entree')
def get_entrees():
    try:
        menu_url = urljoin(SERVER_URL, '/menu')
        response = requests.get(menu_url, timeout=5)
        response.raise_for_status()
        menu_list = response.json()
        entree_list = [item for item in menu_list if item['category'] == 'Entree']
        return jsonify(entree_list)
    except requests.Timeout:
        return {'error': 'Request timed out'}
    except requests.RequestException as e:
        return jsonify({'error': f'{e}'}), 500
    
@app.route('/get_menu/side')
def get_sides():
    try:
        menu_url = urljoin(SERVER_URL, '/menu')
        response = requests.get(menu_url, timeout=5)
        response.raise_for_status()
        menu_list = response.json()
        side_list = [item for item in menu_list if item['category'] == 'Side']
        return jsonify(side_list)
    except requests.Timeout:
        return {'error': 'Request timed out'}
    except requests.RequestException as e:
        return jsonify({'error': f'{e}'}), 500
    
@app.route('/get_menu/dessert')
def get_desserts():
    try:
        menu_url = urljoin(SERVER_URL, '/menu')
        response = requests.get(menu_url, timeout=5)
        response.raise_for_status()
        menu_list = response.json()
        dessert_list = [item for item in menu_list if item['category'] == 'Dessert']
        return jsonify(dessert_list)
    except requests.Timeout:
        return {'error': 'Request timed out'}
    except requests.RequestException as e:
        return jsonify({'error': f'{e}'}), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=5001)