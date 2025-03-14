from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Ejemplo de datos
items = []

# Ruta principal
@app.route('/')
def home():
    return jsonify({"message": "Bienvenido a la API"})

# Obtener todos los items
@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify({"items": items})

# Obtener un item por ID
@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "Item no encontrado"}), 404
    return jsonify({"item": item})

# Crear un nuevo item
@app.route('/api/items', methods=['POST'])
def create_item():
    if not request.json:
        return jsonify({"error": "Datos no válidos"}), 400
    
    new_item = {
        "id": len(items) + 1,
        "name": request.json.get('name'),
        "description": request.json.get('description')
    }
    items.append(new_item)
    return jsonify({"item": new_item}), 201

# Actualizar un item
@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "Item no encontrado"}), 404
    
    item['name'] = request.json.get('name', item['name'])
    item['description'] = request.json.get('description', item['description'])
    return jsonify({"item": item})

# Eliminar un item
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "Item no encontrado"}), 404
    
    items.remove(item)
    return jsonify({"message": "Item eliminado"}), 200

if __name__ == '__main__':
    app.run(debug=True)
