from flask import Flask, request, jsonify
import random
import string

app = Flask(__name__)

# Diccionario para guardar los clientes conectados
conexiones = {}

def generar_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@app.route('/')
def home():
    return "Servidor Acceso Remoto EB funcionando correctamente."

@app.route("/registrar", methods=["POST"])
def registrar():
    id_cliente = generar_id()
    clave = ''.join(random.choices(string.digits, k=4))  # clave de 4 dígitos
    conexiones[id_cliente] = {
        "clave": clave,
        "solicitud": None
    }
    return jsonify({"id": id_cliente, "clave": clave})

@app.route("/solicitar_conexion", methods=["POST"])
def solicitar_conexion():
    data = request.get_json()
    id_destino = data["id_destino"]
    clave = data["clave"]

    if id_destino in conexiones and conexiones[id_destino]["clave"] == clave:
        conexiones[id_destino]["solicitud"] = "pendiente"
        return jsonify({"mensaje": "Solicitud enviada"}), 200
    else:
        return jsonify({"error": "ID no registrado o clave incorrecta"}), 404

@app.route("/verificar_solicitud/<id_destino>")
def verificar_solicitud(id_destino):
    if id_destino in conexiones:
        return jsonify({
            "solicitud": conexiones[id_destino]['solicitud'],
            "clave": conexiones[id_destino]['clave']
        })
    else:
        return jsonify({"error": "ID no registrado"}), 404

@app.route("/responder_solicitud", methods=["POST"])
def responder_solicitud():
    data = request.get_json()
    id_cliente = data["id_cliente"]
    respuesta = data["respuesta"]

    if id_cliente in conexiones:
        conexiones[id_cliente]["solicitud"] = respuesta
        return jsonify({"mensaje": "Respuesta registrada"}), 200
    else:
        return jsonify({"error": "ID no registrado"}), 404

if __name__ == "__main__":
    app.run(debug=True)

