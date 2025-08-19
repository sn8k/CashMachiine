#!/bin/bash
# ui installer v0.3.1 (2025-08-20)
set -e
cd "$(dirname "$0")"
npm install
./install_locales.sh

