resource "google_project_service" "apis" {
  for_each = toset([
    "artifactregistry.googleapis.com",
    "run.googleapis.com",
    "compute.googleapis.com",
    "cloudresourcemanager.googleapis.com",
  ])
  service = each.value

  disable_dependent_services = true
}
