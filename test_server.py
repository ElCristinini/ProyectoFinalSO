import requests

url = "http://127.0.0.1:9559/chat"  # o la IP adecuada, e.g. 192.168.0.104
payload = {"question": "¿Probando servidor?"}

try:
    r = requests.post(url, json=payload, timeout=5)
    r.raise_for_status()
    print("Respuesta del servidor:", r.json())
except Exception as e:
    print("Error al conectar:", e)
