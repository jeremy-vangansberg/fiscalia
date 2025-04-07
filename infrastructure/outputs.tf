output "bucket_name" {
  value = google_storage_bucket.vector_store_bucket.name
}

output "bucket_url" {
  value = "gs://${google_storage_bucket.vector_store_bucket.name}"
}