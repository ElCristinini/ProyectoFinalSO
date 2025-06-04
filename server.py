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

# Prompt personalizado (puedes cambiarlo o hacerlo neutro)
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
