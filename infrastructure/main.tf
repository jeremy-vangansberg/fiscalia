# Active Vertex AI
resource "google_project_service" "vertex_ai" {
  project = var.project_id
  service = "aiplatform.googleapis.com"
}

# Active Cloud Storage
resource "google_project_service" "storage" {
  project = var.project_id
  service = "storage.googleapis.com"
  disable_on_destroy         = true
  disable_dependent_services = true
}

# Bucket GCS pour les vecteurs
resource "google_storage_bucket" "vector_store_bucket" {
  name                        = "${var.project_id}-vector-store"
  location                    = var.region
  uniform_bucket_level_access = true
}

# Création du service principal (service account)
resource "google_service_account" "vertex_sa" {
  account_id   = "vertex-sa"
  display_name = "Vertex AI Service Account"
  project      = var.project_id
}

# Attribution des rôles nécessaires
resource "google_project_iam_member" "vertex_sa_vertex_ai_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.vertex_sa.email}"
}

resource "google_project_iam_member" "vertex_sa_storage_admin" {
  project = var.project_id
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${google_service_account.vertex_sa.email}"
}

resource "google_project_iam_member" "vertex_sa_logging" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.vertex_sa.email}"
}

# Optionnel : pour activer l'authentification ADC depuis un conteneur local, exporter les credentials
output "vertex_sa_email" {
  value = google_service_account.vertex_sa.email
}

resource "google_service_account_key" "vertex_sa_key" {
  service_account_id = google_service_account.vertex_sa.name
  keepers = {
    last_rotation = timestamp()
  }
  public_key_type = "TYPE_X509_PEM_FILE"
  private_key_type = "TYPE_GOOGLE_CREDENTIALS_FILE"
}

resource "local_file" "vertex_sa_key_json" {
  content              = base64decode(google_service_account_key.vertex_sa_key.private_key)
  filename             = "${path.module}/vertex_sa_key.json"
  file_permission      = "0600"
  directory_permission = "0700"
}