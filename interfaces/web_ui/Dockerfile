FROM python:3.11-slim

# Pour éviter les prompts (Streamlit telemetry)
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_SERVER_PORT=8080 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Dépendances système utiles (optionnel : fonts, ssl, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Crée un dossier clean pour l'app
WORKDIR /app

# Copie requirements + install en 2 étapes (pour le cache Docker)
COPY requirements.txt .

RUN pip install -r requirements.txt

# Copie du reste du code Streamlit
COPY . .

EXPOSE 8080

CMD ["streamlit", "run", "app.py"]
