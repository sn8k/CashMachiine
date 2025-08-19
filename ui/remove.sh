#!/bin/bash
# ui removal v0.3.3 (2025-08-19)
set -e
cd "$(dirname "$0")"
rm -rf node_modules .next
./remove_locales.sh

