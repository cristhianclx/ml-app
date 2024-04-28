data "google_iam_policy" "public" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}
resource "google_cloud_run_service_iam_policy" "noauth" {
  location = google_cloud_run_v2_service.server.location
  project  = google_cloud_run_v2_service.server.project
  service  = google_cloud_run_v2_service.server.name

  policy_data = data.google_iam_policy.public.policy_data
}
