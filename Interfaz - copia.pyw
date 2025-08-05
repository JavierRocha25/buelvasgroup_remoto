import tkinter as tk
from tkinter import ttk
import threading
import random
import requests
import os
import subprocess
import sys
import signal

# CONFIGURACIÓN GLOBAL
NGROK_AUTH_TOKEN = "30EofETg1eCfcmGqBRWVulN1ny4_246aNFbXxWB1EiNUaPW6V"
BROKER_LOCAL_PORT = 5000
BROKER_URL = "http://127.0.0.1:5000"  # Usa Ngrok si es necesario

# FUNCIONES PRINCIPALES
def generar_id():
    return str(random.randint(100000000, 999999999))

def iniciar_ngrok():
    if not os.path.exists("ngrok.exe"):
        print("ngrok.exe no encontrado")
        return
    subprocess.Popen(["ngrok.exe", "authtoken", NGROK_AUTH_TOKEN])
    subprocess.Popen(["ngrok.exe", "http", str(BROKER_LOCAL_PORT)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def iniciar_broker():
    def broker():
        os.system(f"pythonw broker.pyw")
    threading.Thread(target=broker, daemon=True).start()

# REGISTRO AUTOMÁTICO AL INICIAR
ID_LOCAL = generar_id()

try:
    requests.post(f"{BROKER_URL}/register", json={"id": ID_LOCAL, "ip": "localhost"})
except:
    pass

import tkinter as tk
from PIL import Image, ImageTk

app = tk.Tk()
app.title("SOPORTE EB")
app.geometry("800x600")
app.configure(bg="#d3d3d3")

# Establecer el ícono de la ventana (en la barra de título)
try:
    icon_img = Image.open("Logo.png")  # Usa tu imagen PNG o ICO
    icon_tk = ImageTk.PhotoImage(icon_img)
    app.iconphoto(False, icon_tk)
except Exception as e:
    print(f"No se pudo establecer el ícono de la ventana: {e}")

from PIL import Image, ImageTk

import tkinter as tk
from PIL import Image, ImageTk

# --- Barra de conexión con logo e input ---
barra_frame = tk.Frame(app, bg="#d3d3d3")
barra_frame.pack(fill="x", padx=10, pady=(10, 0))  # Ancho completo + margen lateral

# Logo pequeño dentro de la barra (opcional)
try:
    logo_barra = Image.open("Logo.png")
    logo_barra = logo_barra.resize((24, 24), Image.LANCZOS)
    logo_barra_tk = ImageTk.PhotoImage(logo_barra)

    logo_label_barra = tk.Label(barra_frame, image=logo_barra_tk, bg="#d3d3d3")
    logo_label_barra.image = logo_barra_tk
    logo_label_barra.pack(side="left", padx=(5, 5))
except Exception as e:
    print(f"No se pudo cargar el logo para la barra: {e}")

# Placeholder en el campo de entrada
placeholder_text = "Introduzca la dirección remota"

def on_entry_focus_in(event):
    if entry_id_remoto.get() == placeholder_text:
        entry_id_remoto.delete(0, tk.END)
        entry_id_remoto.config(fg="black")

def on_entry_focus_out(event):
    if entry_id_remoto.get().strip() == "":
        entry_id_remoto.insert(0, placeholder_text)
        entry_id_remoto.config(fg="gray")

entry_id_remoto = tk.Entry(barra_frame, font=("Segoe UI", 12), fg="gray")
entry_id_remoto.insert(0, placeholder_text)
entry_id_remoto.bind("<FocusIn>", on_entry_focus_in)
entry_id_remoto.bind("<FocusOut>", on_entry_focus_out)
entry_id_remoto.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=4)

# Botón de conexión
btn_conectar = tk.Button(barra_frame, text="Conectar", font=("Segoe UI", 10))
btn_conectar.pack(side="left")

style = ttk.Style()
style.configure("TLabel", background="#d3d3d3", foreground="#004c99", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10))

frame_main = tk.Frame(app, bg="#d3d3d3")
frame_main.pack(pady=30)

from tkinter import font

# Crear fuentes escalables
fuente_texto_peque = font.Font(family="Segoe UI", size=12)
fuente_id_peque = font.Font(family="Segoe UI", size=24, weight="bold")

fuente_texto_grande = font.Font(family="Segoe UI", size=24)
fuente_id_grande = font.Font(family="Segoe UI", size=48, weight="bold")

# Frame contenedor
id_frame = tk.Frame(frame_main, bg="#d3d3d3")
id_frame.pack(pady=20, anchor="w")

# Etiquetas
label_texto = tk.Label(id_frame, text="Mi puesto de trabajo", font=fuente_texto_peque, bg="#d3d3d3", fg="black")
label_id = tk.Label(id_frame, text=f" {ID_LOCAL}", font=fuente_id_peque, bg="#d3d3d3", fg="#0c1a36")

label_texto.pack(side="left")
label_id.pack(side="left")

# Función para ajustar tamaño dinámicamente
def ajustar_tamano(event):
    ancho = app.winfo_width()

    if ancho >= 1200:
        label_texto.config(font=fuente_texto_grande)
        label_id.config(font=fuente_id_grande)
        id_frame.pack_configure(anchor="center")
    else:
        label_texto.config(font=fuente_texto_peque)
        label_id.config(font=fuente_id_peque)
        id_frame.pack_configure(anchor="w")

# Enlazar el evento de cambio de tamaño
app.bind("<Configure>", ajustar_tamano)

frame_historial = tk.LabelFrame(app, text="Sesiones Recientes", bg="#d3d3d3", fg="#004c99", font=("Segoe UI", 10, "bold"))
frame_historial.pack(padx=20, pady=20, fill="both", expand=True)

historial = tk.Listbox(frame_historial, font=("Segoe UI", 10), bg="#f5f5f5", fg="#004c99")
historial.pack(fill="both", expand=True, padx=10, pady=10)

# Agregar ejemplo al historial
historial.insert(tk.END, "192837465 - Oficina Principal")
historial.insert(tk.END, "123456789 - Soporte")

import paho.mqtt.client as mqtt
import json
import pyautogui
import base64
import io
import time
from utilidades import get_local_ip
from ngrok import iniciar_ngrok

def iniciar_transmision_pantalla():
    local_id = get_local_ip()
    topic_screen = f"{local_id}/screen"

    def publicar():
        client = mqtt.Client()
        client.connect("broker.hivemq.com", 1883, 60)
        while True:
            screenshot = pyautogui.screenshot()
            buffer = io.BytesIO()
            screenshot.save(buffer, format="PNG")
            img_data = base64.b64encode(buffer.getvalue())
            client.publish(topic_screen, img_data)
            time.sleep(1)

    threading.Thread(target=publicar, daemon=True).start()

def esperar_solicitud_conexion():
    local_id = get_local_ip()
    topic_solicitud = f"{local_id}/solicitud"
    topic_respuesta = f"{local_id}/respuesta"

    def on_message(client, userdata, msg):
        datos = json.loads(msg.payload.decode())
        remoto = datos.get("desde")

        def mostrar_popup():
            popup = tk.Toplevel(app)
            popup.title("Solicitud de conexión")
            popup.geometry("300x150")
            popup.configure(bg="white")
            tk.Label(popup, text=f"{remoto} desea conectarse.", bg="white").pack(pady=10)

            def aceptar():
                client.publish(topic_respuesta, json.dumps({"respuesta": "aceptado", "para": remoto}))
                popup.destroy()
                iniciar_transmision_pantalla()

            def rechazar():
                client.publish(topic_respuesta, json.dumps({"respuesta": "rechazado", "para": remoto}))
                popup.destroy()

            tk.Button(popup, text="Aceptar", command=aceptar, width=10).pack(pady=5)
            tk.Button(popup, text="Rechazar", command=rechazar, width=10).pack()

        app.after(0, mostrar_popup)

    client = mqtt.Client()
    client.on_message = on_message
    client.connect("broker.hivemq.com", 1883, 60)
    client.subscribe(topic_solicitud)
    client.loop_start()

def cerrar_aplicacion():
    os.kill(os.getpid(), signal.SIGTERM)

# Agregar estos justo antes de app.mainloop()
app.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)
app.after(1000, iniciar_ngrok)

def iniciar_broker():
    def broker():
        os.system("start /B pythonw broker.pyw")
    threading.Thread(target=broker, daemon=True).start()

app.after(1500, iniciar_broker)
app.after(2000, esperar_solicitud_conexion)


app.mainloop()
