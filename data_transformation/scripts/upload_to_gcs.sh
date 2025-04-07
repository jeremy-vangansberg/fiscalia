#!/bin/bash

# === Configuration ===
BUCKET_NAME=fiscalia-455807-vector-store # 🔁 À adapter
DEST_PREFIX="original_data"  # 🔁 Chemin dans le bucket
BASE_PATH="../../data"

# === Fichiers à uploader ===
FILES=(
  "$BASE_PATH/bofip/bofip_documents.jsonl"
  "$BASE_PATH/bofip/bofip_bareme.jsonl"
  "$BASE_PATH/cgi/cgi_documents.jsonl"
)

# === Authentification ===
export GOOGLE_APPLICATION_CREDENTIALS="$CREDENTIALS_PATH"

# Vérifie gsutil
if ! command -v gsutil &> /dev/null; then
    echo "❌ gsutil n'est pas installé. Installe le SDK GCP avec 'gcloud init'."
    exit 1
fi

# Upload des fichiers un par un
for FILE in "${FILES[@]}"; do
    BASENAME=$(basename "$FILE")
    DEST_PATH="gs://$BUCKET_NAME/$DEST_PREFIX/$BASENAME"
    
    echo "🚀 Upload de $FILE → $DEST_PATH"
    gsutil cp "$FILE" "$DEST_PATH"

    if [ $? -eq 0 ]; then
        echo "✅ $BASENAME uploadé avec succès !"
    else
        echo "❌ Échec de l'upload de $BASENAME"
    fi
done
