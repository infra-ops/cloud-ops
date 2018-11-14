resource "google_compute_global_forwarding_rule" "forwarding_rule" {
  name       = "forwarding-rule"
  target     = "${google_compute_target_http_proxy.http_proxy.self_link}"
  port_range = "80"
}

resource "google_compute_target_http_proxy" "http_proxy" {
  name    = "http-proxy"
  url_map = "${google_compute_url_map.urlmap.self_link}"
}

resource "google_compute_url_map" "urlmap" {
  name            = "url-map"
  default_service = "${google_compute_backend_service.internet_lb.self_link}"

  host_rule {
    hosts        = ["*"]
    path_matcher = "allpaths"
  }

  path_matcher {
    name            = "allpaths"
    default_service = "${google_compute_backend_service.internet_lb.self_link}"

    path_rule {
      paths   = ["/"]
      service = "${google_compute_backend_service.internet_lb.self_link}"
    }
  }
}

resource "google_compute_backend_service" "internet_lb" {
  name             = "${var.internet-lb-name}"
  project          = "${var.project-name}"
  port_name        = "http"
  protocol         = "HTTP"
  timeout_sec      = 30
  session_affinity = "NONE"

  backend {
    group = "${google_compute_instance_group.webservers.0.self_link}"
  }

  backend {
    group = "${google_compute_instance_group.webservers.1.self_link}"
  }

  health_checks = ["${google_compute_http_health_check.default.self_link}"]
}

resource "google_compute_http_health_check" "default" {
  name               = "default-hc"
  request_path       = "/"
  check_interval_sec = 1
  timeout_sec        = 1
}
