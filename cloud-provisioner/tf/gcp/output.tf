output "lb_ip" {
  value = "${google_compute_backend_service.internet_lb.self_link}"
}
