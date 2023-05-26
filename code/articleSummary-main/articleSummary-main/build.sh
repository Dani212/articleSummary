#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip --force
pip install -r requirements.txt
