#!/bin/bash
# ui installer v0.3.3 (2025-08-19)
set -e
cd "$(dirname "$0")"
npm install
./install_locales.sh

