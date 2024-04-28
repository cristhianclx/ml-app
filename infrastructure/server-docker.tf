resource "google_artifact_registry_repository" "server" {
  location      = var.location
  repository_id = "docker-${local.slug}"
  format        = "DOCKER"
}
