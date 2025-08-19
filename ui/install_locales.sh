#!/bin/bash
# locale assets installer v0.1.1 (2025-08-19)
set -e
cd "$(dirname "$0")"
mkdir -p public/locales
cp -r locales/* public/locales/
