FROM ubuntu:24.04

# RUN export DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3 python3-dev python3-pip python3-venv \
    # python3-mysqldb
    gcc pkg-config \
    default-libmysqlclient-dev \
    # libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /cata_system

COPY requirements.txt .

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN ls -lah

RUN pip install --upgrade pip && \
    pip install wheel && \
    pip install -r requirements.txt

COPY . .

RUN python3 manage.py migrate
# RUN python3 manage.py tailwind build
# RUN python3 manage.py collectstatic --noinput

RUN python3 manage.py shell < create_superuser.py

EXPOSE 7860

CMD ["python3", "manage.py", "runserver", "0.0.0.0:7860"]