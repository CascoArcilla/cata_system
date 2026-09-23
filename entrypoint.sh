#!/bin/sh

echo "Compilando estilos"
python manage.py tailwind build

echo "Recoleccion de archivos estaticos"
python manage.py collectstatic --noinput

echo "Realizando migraciones necesarias"
python manage.py migrate

echo "Iniciando la aplicacion"
python manage.py runserver 0.0.0.0:8000