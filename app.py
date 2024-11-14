# app.py
from flask import Flask, request, jsonify
from google.cloud import vision
from google.oauth2 import service_account
from io import BytesIO

app = Flask(__name__)

# Inicializar el cliente de Google Cloud Vision
credentials = service_account.Credentials.from_service_account_file(
    "/app/plasma-system-441721-h5-e71c8d0472b7.json"
)
client = vision.ImageAnnotatorClient(credentials=credentials)

@app.route('/extract_text', methods=['POST'])
def extract_text():
    try:
        # Verificar si se ha enviado un archivo
        if 'image' not in request.files:
            return jsonify({"error": "No se envió ningún archivo"}), 400

        # Leer el archivo de imagen enviado
        file = request.files['image']
        image_content = file.read()

        # Crear la imagen para Google Cloud Vision
        image = vision.Image(content=image_content)

        # Realizar la detección de texto
        response = client.text_detection(image=image)
        texts = response.text_annotations

        # Extraer el texto principal si existe
        extracted_text = texts[0].description if texts else ""
        print("Texto extraído:", extracted_text)

        # Verificar si hubo errores en la respuesta
        if response.error.message:
            return jsonify({"error": response.error.message}), 500

        # Retornar el texto extraído
        return jsonify({"text": extracted_text}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
