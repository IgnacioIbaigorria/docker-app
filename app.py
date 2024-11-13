# app.py
from flask import Flask, request, jsonify
from pytesseract import pytesseract
from PIL import Image
import base64
import io

app = Flask(__name__)

# Configura la ruta de Tesseract en Docker
pytesseract.tesseract_cmd = "/usr/bin/tesseract"

@app.route('/extract_text', methods=['POST'])
def extract_text():
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({"error": "No se envió ninguna imagen"}), 400

        # Decodificar la imagen base64
        image_data = base64.b64decode(data['image'])
        image = Image.open(io.BytesIO(image_data))

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
