#!/bin/bash
# db restore utility v0.1.0 (2025-08-19)
set -e

if [[ "$1" == "--install" ]]; then
  mkdir -p backups
  exit 0
fi
if [[ "$1" == "--remove" ]]; then
  rm -rf backups
  exit 0
fi

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <dump_file> [psql args...]" >&2
  exit 1
fi
DUMP_FILE="$1"
shift
psql "$@" < "$DUMP_FILE"
