terraform {
  required_version = ">=1.8.2"

  backend "gcs" {
    bucket = "infrastructure-server-ml-app-demo-pe"
    prefix = "tf"
  }
}
