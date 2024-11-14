import os
import json
from flask import Flask, request, jsonify
from google.cloud import vision
from google.oauth2 import service_account
from io import BytesIO

app = Flask(__name__)

# Crea un archivo temporal para las credenciales usando el contenido de la variable de entorno
credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
credentials_path = "/tmp/google_credentials.json"

# Escribe el contenido de la variable en un archivo
with open(credentials_path, "w") as f:
    f.write(credentials_json)

# Cargar las credenciales
credentials = service_account.Credentials.from_service_account_file(credentials_path)
client = vision.ImageAnnotatorClient(credentials=credentials)

@app.route('/extract_text', methods=['POST'])
def extract_text():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No se envió ningún archivo"}), 400

        file = request.files['image']
        image_content = file.read()

        image = vision.Image(content=image_content)
        response = client.text_detection(image=image)
        texts = response.text_annotations

        extracted_text = texts[0].description if texts else ""
        print("Texto extraído:", extracted_text)

        if response.error.message:
            return jsonify({"error": response.error.message}), 500

        return jsonify({"text": extracted_text}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
