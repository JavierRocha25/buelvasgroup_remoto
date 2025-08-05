from pyngrok import ngrok
import os

def iniciar_ngrok(puerto=5000):
    # Asegúrate de que ngrok esté en la ruta, o proporciona la ruta completa a ngrok.exe
    os.environ["NGROK_PATH"] = "ngrok"  # Si ngrok.exe está en la misma carpeta, esto funciona
    try:
        url = ngrok.connect(puerto, "tcp")
        print(f"Ngrok iniciado en: {url}")
        return url
    except Exception as e:
        print(f"Error iniciando ngrok: {e}")
        return None
