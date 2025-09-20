FROM ubuntu:24.04

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

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r requirements.txt

RUN python manage.py migrate
RUN python manage.py tailwind build
RUN python manage.py collectstatic --noinput

RUN python manage.py shell < create_superuser.py

EXPOSE 7860

CMD ["python3", "manage.py", "runserver", "0.0.0.0:7860"]