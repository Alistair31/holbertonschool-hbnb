#!/bin/bash
set -e

# Install required system packages
PACKAGES_TO_INSTALL=""
python3 -c "import ensurepip" > /dev/null 2>&1 || PACKAGES_TO_INSTALL="$PACKAGES_TO_INSTALL python3.12-venv"
command -v sqlite3 > /dev/null 2>&1 || PACKAGES_TO_INSTALL="$PACKAGES_TO_INSTALL sqlite3"

if [ -n "$PACKAGES_TO_INSTALL" ]; then
    echo "Installing system dependencies:$PACKAGES_TO_INSTALL"
    sudo apt update -qq
    sudo apt install -y $PACKAGES_TO_INSTALL
fi

# Move to the correct folder
cd "$(dirname "$0")/part3/hbnb"

# Create virtual environment if it doesn't exist or is broken
if [ ! -f "venv/bin/activate" ]; then
    echo "Creating virtual environment..."
    rm -rf venv
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --quiet -r app/requirements.txt

# Create instance folder if needed
mkdir -p instance

# Run SQL script to create tables and insert initial data
echo "Setting up database..."
sqlite3 instance/development.db < create_tables.sql

# Launch the app
echo "Starting HBnB API..."
python3 -m app.run
