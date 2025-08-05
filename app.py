from flask import Flask, request, jsonify

app = Flask(__name__)

connections = {}

@app.route('/')
def home():
    return "Servidor de Acceso Remoto EB funcionando"

@app.route('/registrar', methods=['POST'])
def registrar():
    data = request.get_json()
    client_id = data.get('id')
    address = data.get('address')
    if client_id and address:
        connections[client_id] = address
        return jsonify({"status": "registrado"}), 200
    return jsonify({"error": "Datos incompletos"}), 400

@app.route('/solicitar_conexion/<client_id>')
def solicitar_conexion(client_id):
    address = connections.get(client_id)
    if address:
        return jsonify({"address": address})
    return jsonify({"error": "Cliente no encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)