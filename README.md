
# Informe Final: Integración de Chatbot con Pepper
**Curso de Sistemas Operativos**  
_**Ana Vargas y Cristian Olarte**_  
_Fecha: [fecha actual]_

---

## 1. Implementación del Servidor (Código del servidor)

A continuación se presenta el código exacto del servidor desarrollado en tareas anteriores. Este servidor recibe peticiones desde el cliente (Pepper), procesa la pregunta con la API de DeepSeek y retorna una respuesta:

```python
# server.py
from flask import Flask, request, jsonify
import requests

# Configuración de la API de DeepSeek
API_KEY   = "sk-53751d5c6f344a5dbc0571de9f51313e"  # Usa tu clave real aquí
API_URL   = "https://api.deepseek.com/v1/chat/completions"
HEADERS   = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Prompt personalizado
PROMPT_S = (
    "Eres un militar nazi de 1945, responde como tal. "
    "Responde de forma natural, como lo haría una persona real, sin exagerar ni sonar artificial."
)

# Inicializar servidor Flask
app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        pregunta = data.get("question", "")

        if not pregunta.strip():
            return jsonify({"respuesta": "No entendí la pregunta."})

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": PROMPT_S},
                {"role": "user",   "content": pregunta}
            ]
        }

        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()  # Lanzar error si el servidor responde con error
        texto = response.json()["choices"][0]["message"]["content"]

        return jsonify({"respuesta": texto})

    except Exception as e:
        return jsonify({"respuesta": "Error procesando la solicitud: " + str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

## 2. Implementación del Cliente (Pepper)

El siguiente código es el cliente que debe ejecutarse dentro de Pepper. Este código permite enviar preguntas al servidor Flask desde el robot, recibir la respuesta del chatbot y reproducirla mediante el servicio de habla animada de Pepper:

```python
# -- coding: utf-8 --
import qi
import sys
import httplib
import json

# === CONFIGURACION ===
ROBOT_IP = "192.168.0.106"      # IP de tu Pepper
SERVER_IP = "192.168.0.107"     # IP de tu PC (donde corre server.py)
SERVER_PORT = 5000              # Puerto del servidor Flask

# === CONEXION CON PEPPER ===
try:
    session = qi.Session()
    session.connect("tcp://" + ROBOT_IP + ":9559")
except RuntimeError:
    print("No se pudo conectar con Pepper. Verifica la IP.")
    sys.exit(1)

# === SERVICIOS ===
animated_speech = session.service("ALAnimatedSpeech")

# === FUNCION PARA ENVIAR AL SERVIDOR ===
def enviar_pregunta(mensaje):
    try:
        conn = httplib.HTTPConnection(SERVER_IP, SERVER_PORT)
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({"question": mensaje})
        conn.request("POST", "/chat", data, headers)
        response = conn.getresponse()
        respuesta = json.loads(response.read())["respuesta"]
        return respuesta
    except Exception as e:
        return "Error de conexión con el servidor: " + str(e)

# === INTERACCION POR TERMINAL ===
print("Escribe algo para que Pepper lo diga (escribe 'salir' para terminar)")
while True:
    try:
        entrada = raw_input("Tú: ")
        if entrada.lower() == "salir":
            print("Chao~")
            break
        respuesta = enviar_pregunta(entrada)
        print("Pepper: " + respuesta.encode('utf-8'))  # ✅ CORREGIDO: evita error de unicode
        animated_speech.say(respuesta)
    except KeyboardInterrupt:
        print("
Terminando...")
        break
```

---

## 3. Solución para la Conexión con Pepper y el Servidor

Para asegurar que la conexión entre Pepper y el servidor funcione correctamente, sigue estos pasos:

1. **Verificar las IPs:**
   Asegúrate de que tanto Pepper como el servidor estén en la misma red o que las IPs configuradas en el código sean correctas.
   - Para Pepper: Verifica la IP de tu dispositivo Pepper con `ifconfig` o revisando el manual del dispositivo.
   - Para el servidor: Verifica que la IP de tu máquina local (donde corre el servidor Flask) esté bien configurada.

2. **Configurar el servidor Flask:**
   Asegúrate de que el servidor Flask esté corriendo en la IP correcta y en el puerto especificado (en este caso, `5000`).
   - Ejecuta `python server.py` en la máquina donde corre el servidor Flask.
   - Revisa que no haya problemas de firewall que puedan bloquear las conexiones al puerto `5000`.

3. **Conexión a Pepper:**
   En el código del cliente (`Pepper`), asegúrate de que la dirección IP de Pepper (`ROBOT_IP`) sea correcta y accesible desde tu máquina.
   - Si tienes problemas con la conexión, intenta usar `ping` para verificar si la máquina puede comunicarse con Pepper.

4. **Prueba de Conexión:**
   Si todo está bien configurado, ejecuta ambos códigos:
   - El servidor Flask en la máquina local.
   - El código en Pepper.
   - Intenta enviar preguntas desde la terminal de Pepper y verifica que el servidor esté respondiendo correctamente.

5. **Depuración:**
   Si experimentas errores, revisa los logs de ambas máquinas:
   - En la terminal de la máquina local para el servidor Flask.
   - En la terminal de Pepper si el cliente no puede conectarse.
   - Asegúrate de que no haya bloqueos de puertos o IPs.

---
