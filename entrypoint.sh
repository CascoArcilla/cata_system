#!/bin/sh

echo "Compilando estilos"
python3 manage.py tailwind build

echo "Recoleccion de archivos estaticos"
python3 manage.py collectstatic --noinput

echo "Realizando migraciones necesarias"
python3 manage.py migrate

echo "Creando superusuario si no existe"
./create_superuser.sh

echo "Iniciando la aplicacion"
python3 manage.py runserver 0.0.0.0:8000