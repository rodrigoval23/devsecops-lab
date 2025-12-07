# Creamos el Dockerfile para que Jenkins pueda desplegar la app
cat <<EOF > app/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copiamos dependencias e instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

# Exponemos el puerto de Flask
EXPOSE 5000

# Ejecutamos la app
CMD ["python", "web_app.py"]
EOF
