import json
import subprocess
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import paho.mqtt.client as mqtt

mensajes1 = ""
mensajes2 = ""
mensajes3 = ""
mensajes4 = ""

# Configuración del broker MQTT
mqtt_broker = "localhost"  # Dirección IP del broker MQTT
mqtt_port = 1883  # Puerto del broker MQTT

app = Flask(__name__)
CORS(app)


# Conexión al broker MQTT
mqtt_client = mqtt.Client()

mqtt_client.connect(mqtt_broker, mqtt_port, 60)

def on_connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT")
    client.subscribe("led_control1")  # Suscribirse al topic "led/control1" para el LED 1
    client.subscribe("led_control2")  # Suscribirse al topic "led/control2" para el LED 2
    
    client.subscribe("temperatura")  # Suscribirse al topic "led/control2" para el LED 2
    client.subscribe("humedad")  # Suscribirse al topic "led/control2" para el LED 2

def on_message(client, userdata, msg):
    global mensajes1
    global mensajes2
    global mensajes3
    global mensajes4

    if msg.topic == "led_control1":
        mensajes1 = msg.payload
    elif msg.topic == "led_control2":
        mensajes2 = msg.payload
    elif msg.topic == "temperatura":
        mensajes3 = msg.payload
    elif msg.topic == "humedad":
        mensajes4 = msg.payload
    else:
        print("mensaje no identificado")
    
    print(f"Mensaje recibido: {msg.topic} - {msg.payload}")

#def on_message(client, userdata, msg):
# payload = json.loads(msg.payload.decode())
 #   mensajes.append(payload)

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/encender1')
def encender1():
    mqtt_client.publish("led_control1", "ON")
    return "LED 1 encendido"

@app.route('/apagar1')
def apagar1():
    mqtt_client.publish("led_control1", "OFF")
    return "LED 1 apagado"

@app.route('/encender2')
def encender2():
    mqtt_client.publish("led_control2", "ON")
    return "LED 2 encendido"

@app.route('/apagar2')
def apagar2():
    mqtt_client.publish("led_control2", "OFF")
    return "LED 2 apagado"

ultimo_mensaje = None


@app.route('/led1', methods=['GET'])
def obtener_mensajes_mqtt():
    return (mensajes1)

@app.route('/led2', methods=['GET'])
def obtener_mensajes_mqtt2():
    return (mensajes2)

@app.route('/temperatura', methods=['GET'])
def obtener_mensajes_mqtt3():
    return (mensajes3)

@app.route('/humedad', methods=['GET'])
def obtener_mensajes_mqtt4():
    return (mensajes4)

if __name__ == '__main__':
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(mqtt_broker, mqtt_port)
    mqtt_client.loop_start()
    app.run(debug=True, host='192.168.137.217',port=4000)
