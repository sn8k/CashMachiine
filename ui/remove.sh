#!/bin/bash
# ui removal v0.3.4 (2025-08-20)
set -e
cd "$(dirname "$0")"
rm -rf node_modules .next
./remove_locales.sh
