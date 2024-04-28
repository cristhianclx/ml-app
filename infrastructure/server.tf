resource "google_cloud_run_v2_service" "server" {
  name         = local.slug
  location     = var.location
  ingress      = "INGRESS_TRAFFIC_ALL"
  launch_stage = "BETA"

  template {
    containers {
      resources {
        limits = {
          cpu    = "2"
          memory = "1024Mi"
        }
      }
      image = "${google_artifact_registry_repository.server.location}-docker.pkg.dev/${local.slug}/${google_artifact_registry_repository.server.repository_id}/${var.website}:${var.stage}"
      ports {
        container_port = 8000
      }
      liveness_probe {
        http_get {
          path = "/health"
        }
      }
      volume_mounts {
        name       = "data"
        mount_path = "/data"
      }
    }
    volumes {
      name = "data"
      gcs {
        bucket    = google_storage_bucket.server.name
        read_only = false
      }
    }
    timeout                          = "120s"
    max_instance_request_concurrency = 100
  }
}
