# Usa una imagen base de Python ligera
FROM python:3.8-slim

# Configura el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de la aplicación al contenedor
COPY . /app

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Establece la variable de entorno para las credenciales de Google Cloud
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/plasma-system-441721-h5-e71c8d0472b7.json"

# Expone el puerto 5000 para Flask
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
