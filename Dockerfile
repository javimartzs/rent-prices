# Añadimos la imagen de Python
FROM python:3.12-slim

# Establecemos el directorio de trabajo en el contenedor 
WORKDIR /app

# Copiare el archivo de requerimientos al contenedor 
COPY folder /app

# INstalar las dependencias en 
RUN pip install --no-cache-dir -r /app/requirements.txt

# Establecer el directorio de trabajo donde reside el código del pipeline
WORKDIR /app/code


# Ejecutar el script principal que orquesta el pipeline ETL
CMD ["python", "pipeline.py"]