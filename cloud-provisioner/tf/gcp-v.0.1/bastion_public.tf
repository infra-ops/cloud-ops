resource "google_compute_instance" "bastion-instance" {
  name         = "${var.bastion-instance-name}"
  machine_type = "${var.vm_type["512gig"]}"

  zone = "${var.zones["zone0"]}"

  tags = [
    "nat-instance",
    "${var.network}-bastion-firewall-ssh",
    "${var.network}-bastion-firewall-http",
    "${var.network}-bastion-firewall-https",
    "${var.network}-bastion-firewall-icmp",
  ]

  boot_disk {
    initialize_params {
      image = "${var.os}"
    }
  }

  metadata {
    hostname = "${var.hostname["host2"]}"
  }

  can_ip_forward = true

  network_interface {
    subnetwork = "${google_compute_subnetwork.my_public_subnetwork.name}"

    access_config {
      // Ephemeral IP
    }
  }
}
