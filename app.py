# app.py
from flask import Flask, request, jsonify
from pytesseract import pytesseract
from PIL import Image
import base64
from io import BytesIO

app = Flask(__name__)

# Configura la ruta de Tesseract en Docker
pytesseract.tesseract_cmd = "/usr/bin/tesseract"

@app.route('/extract_text', methods=['POST'])
def extract_text():
    try:
        # Obtener y decodificar la imagen en base64
        data = request.get_json()
        img_data = data.get('image_base64')
        image = Image.open(BytesIO(base64.b64decode(img_data)))

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
