#!/bin/bash
set -e

# Move to the correct folder
cd "$(dirname "$0")/part3/hbnb"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
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
