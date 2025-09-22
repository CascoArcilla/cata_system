FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3 python3-dev python3-pip python3-venv \
    gcc pkg-config \
    default-libmysqlclient-dev \
    nodejs npm \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /cata_system

RUN npm install -g pnpm

COPY requirements.txt .

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip && \
    pip install wheel && \
    pip install -r requirements.txt

COPY . .

RUN python3 manage.py tailwind install
RUN python3 manage.py tailwind build
RUN python manage.py collectstatic --noinput

EXPOSE 7860

CMD ["python3", "manage.py", "runserver", "0.0.0.0:7860"]