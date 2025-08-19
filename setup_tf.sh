#!/bin/bash
# terraform setup v0.1.0 (2025-08-19)
set -e
TF_DIR="infra/terraform"
LOG_DIR="$TF_DIR/logs"
mkdir -p "$LOG_DIR"
terraform -chdir="$TF_DIR" init > "$LOG_DIR/init.log"
terraform -chdir="$TF_DIR" plan -state="$LOG_DIR/terraform.tfstate" -out="$LOG_DIR/plan.out" > "$LOG_DIR/plan.log"
terraform -chdir="$TF_DIR" apply -auto-approve -state="$LOG_DIR/terraform.tfstate" "$LOG_DIR/plan.out" > "$LOG_DIR/apply.log"
