provider "google" {
  credentials = "${file("account.json")}"
  project     = "${var.project-name}"
  region      = "${var.region}"
  version     = "1.19.0"
}
