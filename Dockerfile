FROM debian:12.10

RUN apt -y update
RUN apt install -y python3 python3-pip python3-mysqldb
# python3-django

WORKDIR /app

COPY . .
RUN ls
RUN pip --version
RUN python3 --version

RUN chmod 777 ./requirements.txt
RUN pip install -r ./requirements.txt

RUN python3 manage.py migrate

RUN chmod 777 ./create_superuser.py
RUN python manege.py shell < create_superuser.py

CMD ["gunicorn", "cata_system.wsgi:tecnicas", "--bind", "0.0.0.0:7860"]
    
# python3 manage.py runserver 0:7860; \

# FROM python:3.11-slim

# WORKDIR /app

# RUN ls

# COPY requirements.txt .

# RUN pip install -r --upgrade pip

# RUN ls

# RUN pip install -r requirements.txt

# COPY . .

# RUN python manege.py migrate

# RUN python manage.py tailwind build

# RUN python manage.py collectstatic --noinput

# RUN python manege.py shell < create_superuser.py

# EXPOSE 7860

# # Comando de inicio (usar gunicorn en vez de runserver en producción)
# CMD ["gunicorn", "cata_system.wsgi:tecnicas", "--bind", "0.0.0.0:7860"]
