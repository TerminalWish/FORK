from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from urllib.parse import urljoin
import requests

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

SERVER_URL = 'http://localhost:5000'

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
        
        # Broadcast the updated order data to all connected clientspyth
        socketio.emit('order_update', order_data)
        return jsonify({'status': 'Update received and broadcasted'}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve or broadcast order data', 'details': str(e)}), 500
    
@socketio.on('connect')
def handle_connect():
    print("Client connected")


# Client connection endpoint
@app.route('/')
def index():
    return "<h1>Knife Server is running. Connect via WebSocket for updates.</h1>"

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5002)
