resource "google_compute_instance" "compute-instance" {
  count        = 2
  name         = "${var.instance-name}-${count.index}"
  machine_type = "${var.vm_type["512gig"]}"

  zone = "${lookup(var.zones, "zone${count.index}")}"

  tags = [
    "private-instances",
    "${var.network}-firewall-ssh",
    "${var.network}-firewall-http",
    "${var.network}-firewall-https",
    "${var.network}-firewall-icmp",
  ]

  boot_disk {
    initialize_params {
      image = "${var.os}"
    }
  }

  metadata {
    hostname = "${lookup(var.hostname, "host${count.index}")}"
  }

  can_ip_forward = true

  network_interface {
    subnetwork = "${google_compute_subnetwork.my_private_subnetwork.name}"
  }
}

resource "google_compute_instance_group" "webservers" {
  count       = 2
  name        = "webserver-group-${count.index}"
  description = "Instance group for compute instances"
  network     = "${google_compute_network.my_network.self_link}"
  instances   = ["${element(google_compute_instance.compute-instance.*.self_link, count.index)}"]
  zone        = "${lookup(var.zones, "zone${count.index}")}"

  named_port {
    name = "http"
    port = "80"
  }

  named_port {
    name = "https"
    port = "443"
  }
}
