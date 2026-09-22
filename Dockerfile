FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
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

RUN sed -i "s|NPM_BIN_PATH = os.getenv('NPM_BIN_PATH', 'pnpm')|NPM_BIN_PATH = 'pnpm'|" cata_system/settings.py

RUN cd theme/static_src && pnpm approve-builds @tailwindcss/oxide && pnpm install && cd /cata_system && python3 manage.py tailwind install

EXPOSE 8000

COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]