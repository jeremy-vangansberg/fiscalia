#!/bin/bash

# ---------------------
# CONFIGURATION
# ---------------------
PROJECT_ID="fiscalia-455807"
REGION="europe-west1"
LOCATION="europe-west1"
REPO_NAME="fiscalia-images"

SERVICE_NAME_API="fiscalia-api"
SERVICE_NAME_UI="fiscalia-ui"
SA_NAME="fiscalia-cloudrun"
SA_EMAIL="$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com"
SECRET_NAME="fiscalia-sa-key"
CREDENTIALS_FILE="api/app/credentials/credentials.json"

API_IMAGE="$LOCATION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME_API"
UI_IMAGE="$LOCATION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME_UI"

# ---------------------
# INIT GCP ENV
# ---------------------
echo "📡 Configuration du projet GCP..."
gcloud config set project "$PROJECT_ID"

echo "🛠️ Activation des APIs nécessaires..."
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  aiplatform.googleapis.com \
  secretmanager.googleapis.com

echo "🔐 Authentification Docker avec Artifact Registry..."
gcloud auth configure-docker "$LOCATION-docker.pkg.dev" --quiet

# ---------------------
# CREATION DU REPO ARTIFACT REGISTRY SI BESOIN
# ---------------------
echo "📦 Vérification du dépôt Artifact Registry ($REPO_NAME)..."
if ! gcloud artifacts repositories describe "$REPO_NAME" --location="$LOCATION" &>/dev/null; then
  echo "🆕 Création du dépôt Artifact Registry : $REPO_NAME"
  gcloud artifacts repositories create "$REPO_NAME" \
    --repository-format=docker \
    --location="$LOCATION" \
    --description="Repo Docker pour Fiscalia"
else
  echo "✅ Dépôt Artifact Registry déjà existant."
fi

# ---------------------
# COMPTE DE SERVICE
# ---------------------
echo "🔐 Vérification du compte de service : $SA_EMAIL"
if ! gcloud iam service-accounts describe "$SA_EMAIL" &>/dev/null; then
  echo "🆕 Création du compte de service..."
  gcloud iam service-accounts create "$SA_NAME" \
    --display-name "Cloud Run Service Account for Fiscalia"

  until gcloud iam service-accounts describe "$SA_EMAIL" &>/dev/null; do
    echo "⏳ Attente propagation IAM..."
    sleep 2
  done
else
  echo "✅ Le compte de service existe déjà."
fi

echo "🔒 Attribution des rôles IAM requis..."
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/aiplatform.user" \
  --quiet

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/secretmanager.secretAccessor" \
  --quiet



# ---------------------
# BUILD + PUSH DES IMAGES
# ---------------------
echo "🚧 Build de l'image API..."
docker build --platform linux/amd64 -t "$API_IMAGE" -f api/Dockerfile ./api
echo "📤 Push de l'image API..."
docker push "$API_IMAGE"

echo "🚧 Build de l'image UI..."
docker build --platform linux/amd64 -t "$UI_IMAGE" -f web_ui/Dockerfile ./web_ui
echo "📤 Push de l'image UI..."
docker push "$UI_IMAGE"


gcloud run services add-iam-policy-binding "$SERVICE_NAME_API" \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/run.invoker" \
  --region="$REGION"

# ---------------------
# DEPLOIEMENT CLOUD RUN
# ---------------------
echo "🚀 Déploiement API sur Cloud Run..."
gcloud run deploy "$SERVICE_NAME_API" \
  --image "$API_IMAGE" \
  --platform managed \
  --region "$REGION" \
  --no-allow-unauthenticated \
  --service-account "$SA_EMAIL" \
  --set-env-vars PROJECT_ID=$PROJECT_ID,MODEL_NAME_EMBEDDING=text-embedding-004,MODEL_NAME_LLM=gemini-2.0-flash-lite,TEMPERATURE_LLM=0,LOCATION=$LOCATION \
  --memory 2Gi

  # --set-secrets GOOGLE_APPLICATION_CREDENTIALS=$SECRET_NAME:latest

# Récupération de l'URL de l'API
echo "🌐 Récupération de l'URL de l'API..."
API_URL=$(gcloud run services describe "$SERVICE_NAME_API" \
  --platform managed \
  --region "$REGION" \
  --format="value(status.url)")

echo "🔗 API URL: $API_URL"

# Déploiement UI avec l'URL dynamique
echo "🚀 Déploiement UI sur Cloud Run..."
gcloud run deploy "$SERVICE_NAME_UI" \
  --image "$UI_IMAGE" \
  --platform managed \
  --region "$REGION" \
  --allow-unauthenticated \
  --set-env-vars API_URL="$API_URL/ask",USE_AUTH=true

# gcloud beta run domain-mappings create \
#   --service="$SERVICE_NAME_UI" \
#   --domain="fiscalia.cloud"\
#   --region="$REGION"

echo "✅ Déploiement terminé avec succès ! 🎉"
