FROM jenkins/jenkins:lts-jdk17

USER root

# 1. Actualizar e instalar dependencias necesarias (Docker CLI y Python3/Pip)
RUN apt-get update &&     apt-get install -y docker.io python3 python3-pip python3-venv

# 2. Agregar el usuario jenkins al grupo docker (para que pueda usar el socket)
RUN usermod -aG docker jenkins

# 3. (Opcional) Limpiar caché para que la imagen pese menos
RUN apt-get clean

USER jenkins
