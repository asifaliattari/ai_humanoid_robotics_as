#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Run database migrations (if using Alembic)
# Uncomment the line below if you have migrations set up
# alembic upgrade head

echo "Build completed successfully!"
