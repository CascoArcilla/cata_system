FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /cata_system

COPY requirements.txt .

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN ls -lah

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

RUN python manage.py migrate
RUN python manage.py tailwind build
RUN python manage.py collectstatic --noinput

RUN python manage.py shell < create_superuser.py

EXPOSE 7860

CMD ["python3", "manage.py", "runserver", "0.0.0.0:7860"]

#########

# FROM python:3.11-slim

# # Instalar dependencias del sistema
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libpq-dev \
#     python3-dev \
#     && rm -rf /var/lib/apt/lists/*

# # Establecer directorio de trabajo
# WORKDIR /app

# # Copiar requirements primero para cachear dependencias
# COPY requirements.txt .

# # Crear y activar entorno virtual
# RUN python -m venv /opt/venv
# ENV PATH="/opt/venv/bin:$PATH"

# # Instalar dependencias de Python
# RUN pip install --upgrade pip && \
#     pip install -r requirements.txt

# # Copiar el resto de la aplicación
# COPY . .

# # Exponer puerto
# EXPOSE 7860

# # Comando para ejecutar la aplicación
# CMD ["python", "manage.py", "runserver", "0.0.0.0:7860"]

# FROM debian:12.10

# RUN apt -y update
# RUN apt install -y python3 python3-pip python3-mysqldb

# RUN PIP_BREAK_SYSTEM_PACKAGES=1

# WORKDIR /app

# COPY . .

# RUN pip install -r ./requirements.txt

# RUN python3 manage.py migrate

# RUN python manege.py shell < create_superuser.py

# CMD ["python3", "manage.py", "runserver", "0.0.0.0:7860"]
# CMD ["gunicorn", "cata_system.wsgi:tecnicas", "--bind", "0.0.0.0:7860"]
    
