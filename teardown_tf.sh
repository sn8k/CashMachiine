#!/bin/bash
# terraform teardown v0.1.0 (2025-08-19)
set -e
TF_DIR="infra/terraform"
LOG_DIR="$TF_DIR/logs"
mkdir -p "$LOG_DIR"
terraform -chdir="$TF_DIR" destroy -auto-approve -state="$LOG_DIR/terraform.tfstate" > "$LOG_DIR/destroy.log"
