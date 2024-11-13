# app.py
from flask import Flask, request, jsonify
from pytesseract import pytesseract
from PIL import Image
import os

app = Flask(__name__)

# Configura la ruta de Tesseract en Docker
pytesseract.tesseract_cmd = "/usr/bin/tesseract"

@app.route('/extract_text', methods=['POST'])
def extract_text():
    try:
        # Verificar si se ha enviado un archivo
        if 'image' not in request.files:
            return jsonify({"error": "No se envió ningún archivo"}), 400

        # Leer el archivo de imagen enviado
        file = request.files['image']
        image = Image.open(file)

        # Extraer texto con Tesseract OCR
        extracted_text = pytesseract.image_to_string(image)
        print("Texto extraído:", extracted_text)

        # Retornar el texto extraído
        return jsonify({"text": extracted_text}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
