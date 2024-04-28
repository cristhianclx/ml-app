resource "google_storage_bucket" "server" {
  name     = "data-${local.slug}"
  location = var.location
}
