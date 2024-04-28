resource "google_cloud_run_domain_mapping" "server" {
  name     = var.website
  location = google_cloud_run_v2_service.server.location
  metadata {
    namespace = data.google_project.project.project_id
  }
  spec {
    route_name = google_cloud_run_v2_service.server.name
  }
}
