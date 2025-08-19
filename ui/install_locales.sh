#!/bin/bash
# locale assets installer v0.1.0 (2025-08-20)
set -e
cd "$(dirname "$0")"
mkdir -p public/locales
cp -r locales/* public/locales/
