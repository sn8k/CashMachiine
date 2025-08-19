# Terraform root module v0.1.0 (2025-08-19)

module "db" {
  source = "./db"
}

module "cache" {
  source = "./cache"
}

module "message_bus" {
  source = "./message_bus"
}

module "services" {
  source = "./services"
}
