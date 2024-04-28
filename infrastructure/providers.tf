terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5"
    }
  }
}

provider "google" {
  project = local.slug
  region  = var.location
}
