resource "google_app_engine_application" "app" {
  project     = "${var.project-name}"
  location_id = "us-east1"
}
