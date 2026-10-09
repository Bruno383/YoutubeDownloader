
FROM python:3.12-slim

# Dependências do FFmpeg, Node.js e compilação do provedor
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    ca-certificates \
    bash \
    git \
    python3 \
    make \
    g++ \
    pkg-config \
    libcairo2-dev \
    libpango1.0-dev \
    libjpeg-dev \
    libgif-dev \
    librsvg2-dev \
    && curl -fsSL https://deb.nodesource.com/setup_22.x -o /tmp/nodesource_setup.sh \
    && bash /tmp/nodesource_setup.sh \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/* /tmp/nodesource_setup.sh

WORKDIR /app

# Instala as dependências Python, incluindo o plugin PO Token
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Baixa e compila o servidor oficial de PO Token, versão 2.0.2
RUN git clone --depth 1 --single-branch --branch 2.0.2 \
    https://github.com/Brainicism/bgutil-ytdlp-pot-provider.git \
    /opt/bgutil-ytdlp-pot-provider \
    && cd /opt/bgutil-ytdlp-pot-provider/server \
    && npm ci \
    && npx tsc

COPY . .

EXPOSE 10000

# Inicia o provedor localmente e depois o aplicativo Flask via Gunicorn
CMD ["bash", "-lc", "node /opt/bgutil-ytdlp-pot-provider/server/build/main.js --host 127.0.0.1 --port 4416 & exec gunicorn --bind 0.0.0.0:10000 --timeout 600 --graceful-timeout 30 app:app"]