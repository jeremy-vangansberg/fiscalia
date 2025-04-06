resource "google_project_iam_member" "vertex_ai_roles" {
  for_each = toset([
    "roles/aiplatform.user",
    "roles/storage.objectAdmin",
  ])
  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.vertex_ai_sa.email}"
}

resource "google_service_account_key" "vertex_ai_key" {
  service_account_id = google_service_account.vertex_ai_sa.name
}

resource "local_file" "vertex_ai_key_file" {
  content  = base64decode(google_service_account_key.vertex_ai_key.private_key)
  filename = "${path.module}/vertex_ai_key.json"
}
