resource "google_compute_firewall" "bastion_allow_ssh" {
  name    = "${var.network}-bastion-firewall-ssh"
  network = "${google_compute_network.my_network.name}"
  project = "${var.project-name}"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  target_tags   = ["${var.network}-bastion-firewall-ssh"]
  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_firewall" "compute_allow_ssh" {
  name    = "${var.network}-firewall-ssh"
  network = "${google_compute_network.my_network.name}"
  project = "${var.project-name}"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  target_tags   = ["${var.network}-firewall-ssh"]
  source_ranges = ["10.0.0.0/16"]
}

resource "google_compute_firewall" "compute_allow_http" {
  name    = "${var.network}-firewall-http"
  network = "${google_compute_network.my_network.name}"
  project = "${var.project-name}"

  allow {
    protocol = "tcp"
    ports    = ["80"]
  }

  target_tags   = ["${var.network}-firewall-http"]
  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_firewall" "compute_allow_https" {
  name    = "${var.network}-firewall-https"
  network = "${google_compute_network.my_network.name}"
  project = "${var.project-name}"

  allow {
    protocol = "tcp"
    ports    = ["443"]
  }

  target_tags   = ["${var.network}-firewall-https"]
  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_firewall" "allow_icmp" {
  name    = "${var.network}-firewall-icmp"
  network = "${google_compute_network.my_network.name}"
  project = "${var.project-name}"

  allow {
    protocol = "icmp"
  }

  target_tags   = ["${var.network}-firewall-icmp"]
  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_firewall" "allow_all_internal" {
  name    = "${var.network}-firewall-all-internal"
  network = "${google_compute_network.my_network.name}"
  project = "${var.project-name}"

  allow {
    protocol = "all"
  }

  source_ranges = ["10.0.0.0/16"]
}
