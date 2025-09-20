FROM python:3.11-slim

WORKDIR /app

RUN ls

COPY . .

RUN ls

RUN python -m pip install --no-cache-dir -r requirements.txt

RUN python manege.py migrate

RUN python manage.py tailwind build

RUN python manage.py collectstatic --noinput

RUN python manege.py shell < create_superuser.py

EXPOSE 7860

# Comando de inicio (usar gunicorn en vez de runserver en producción)
CMD ["gunicorn", "cata_system.wsgi:tecnicas", "--bind", "0.0.0.0:7860"]
