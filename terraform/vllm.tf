# Questo codice è compatibile con Terraform 4.25.0 e versioni precedenti compatibili con 4.25.0.
# Per informazioni sulla convalida di questo codice Terraform, visita la pagina https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/google-cloud-platform-build#format-and-validate-the-configuration
terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.8.0"
    }
  }
}

provider "google" {
  project = var.project
  region  = "us-central1"
  zone    = "us-central1-f"
}

variable "project" {
  type = string
}

resource "google_compute_instance" "vllm-instance" {
  boot_disk {
    auto_delete = true
    device_name = "vllm-instance"

    initialize_params {
      image = "projects/ml-images/global/images/c0-deeplearning-common-cu124-v20250325-debian-11-py310-conda"
      size  = 50
      type  = "pd-balanced"
    }

    mode = "READ_WRITE"
  }

  can_ip_forward      = false
  deletion_protection = false
  enable_display      = false

  guest_accelerator {
    count = 1
    type  = "projects/${var.project}/zones/us-central1-f/acceleratorTypes/nvidia-tesla-t4"
  }

  labels = {
    goog-ec-src = "vm_add-tf"
  }

  machine_type = "n1-standard-2"
  name         = "vllm-instance"

  network_interface {
    access_config {
      network_tier = "PREMIUM"
    }

    queue_count = 0
    stack_type  = "IPV4_ONLY"
    subnetwork  = "projects/${var.project}/regions/us-central1/subnetworks/default"
  }

  scheduling {
    automatic_restart   = true
    on_host_maintenance = "TERMINATE"
    preemptible         = false
    provisioning_model  = "STANDARD"
  }

  service_account {
    email  = "255565253097-compute@developer.gserviceaccount.com"
    scopes = ["https://www.googleapis.com/auth/devstorage.read_only", "https://www.googleapis.com/auth/logging.write", "https://www.googleapis.com/auth/monitoring.write", "https://www.googleapis.com/auth/service.management.readonly", "https://www.googleapis.com/auth/servicecontrol", "https://www.googleapis.com/auth/trace.append"]
  }

  shielded_instance_config {
    enable_integrity_monitoring = true
    enable_secure_boot          = false
    enable_vtpm                 = true
  }

  tags = ["https-server"]
  zone = "us-central1-f"
}