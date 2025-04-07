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

# Bucket GCS pour tes vecteurs
resource "google_storage_bucket" "vector_store_bucket" {
  name                        = "${var.project_id}-vector-store"
  location                    = var.region
  uniform_bucket_level_access = true
}