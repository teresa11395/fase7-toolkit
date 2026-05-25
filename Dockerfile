# Imagen base oficial de Python con Alpine (ligera y segura)
FROM python:3.11-alpine

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos primero solo requirements.txt para aprovechar la caché
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

# Exponemos el puerto 8000
EXPOSE 8000

# Comando para arrancar la API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]