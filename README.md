
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

## 3. Perfil Profesional en GitHub

Aquí se muestra el proceso del perfil profesional en Github, ya que queda mejor visualmente al momento de que personas ajenas a nosotros entren a nuestro perfil:

### Primer Punto:

Crearemos un `README` especial con nuestro nombre de GitHub. Esto hace que podamos editar la presentación de nuestro perfil, quedando de la siguiente manera:

![Imagen](Foto 1.jpg)  
_Imagen de como quedaría de creado el repositorio con nuestro nombre_

### Segundo Punto:

Entraremos al `README` especial con nuestro nombre de GitHub, y ahora entraremos al link que hay en la tarea de Moodle, esto para seleccionar de entre los miles de diseños que hay en ese repositorio en específico:

![Imagen](Imagen 2.jpg)  
_Seleccionaremos alguno de todos los repositorios. Tener en cuenta que en la imagen se ven solo algunos de todos los que hay._

### Tercer Punto:

Copiaremos algún estilo que nos guste y lo pegaremos en el `README`, para esto editaremos el mismo desde un simbolito de un lápiz a la parte derecha de la pantalla. Ya cuando tengamos eso, editaremos y cambiaremos con base en nuestros gustos:

![Imagen](Foto 3.jpg)  
_Tener en cuenta los lenguajes de donde se copió el diseño de GitHub, comúnmente son: HTML, Markdown, etc._

---

## 4. Cuarto Punto:

Ya para terminar, decidiremos si podremos nuestras redes sociales, lo que nos gusta hacer, hobbies, expectativas con las materias, etc., en el mismo, quedando de la siguiente manera:

![Imagen](Foto 4.jpg)  
_Perfil en GitHub 1_

![Imagen](Foto 5.jpg)  
_Perfil en GitHub 2_

![Imagen](Foto 6.jpg)  
_Perfil en GitHub 3_

---
