resource "google_compute_network" "my_network" {
  name                    = "${var.network}"
  project                 = "${var.project-name}"
  description             = "Main global VPC"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "my_public_subnetwork" {
  name          = "${var.network}-public-subnetwork-${var.subnetwork-region}"
  region        = "${var.subnetwork-region}"
  network       = "${google_compute_network.my_network.self_link}"
  ip_cidr_range = "${var.public-cidr}"
}

resource "google_compute_subnetwork" "my_private_subnetwork" {
  name                     = "${var.network}-private-subnetwork-${var.subnetwork-region}"
  region                   = "${var.subnetwork-region}"
  network                  = "${google_compute_network.my_network.self_link}"
  ip_cidr_range            = "${var.private-cidr}"
  private_ip_google_access = true
}

resource "google_compute_route" "nat_route" {
  name                   = "nat-route"
  dest_range             = "0.0.0.0/0"
  network                = "${google_compute_network.my_network.name}"
  next_hop_instance      = "${google_compute_instance.bastion-instance.self_link}"
  next_hop_instance_zone = "${google_compute_instance.bastion-instance.zone}"
  tags                   = ["private-instances"]
  priority               = 100
}
