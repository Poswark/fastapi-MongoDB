# Utiliza una imagen Python más ligera
FROM python:3.8-slim

# Crea el directorio de la aplicación
RUN mkdir /app
WORKDIR /app

# Copia el código fuente al contenedor
COPY code .
COPY requirements.txt .

# Instala las dependencias necesarias y herramientas adicionales
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libc-dev

# Actualiza pip e instala las dependencias
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
WORKDIR /app
# Exponer el puerto en el que la aplicación se ejecutará
EXPOSE 5000

# Comando para ejecutar la aplicación FastAPI
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]

