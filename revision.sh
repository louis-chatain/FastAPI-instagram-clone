#!/bin/bash
set -e

# 1. Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    exit 1
fi

# 2. Optional: Check if a specific variable exists in .env
if ! grep -q "DB_URL" .env; then
    echo "Error: DB_URL not defined in .env"
    exit 1
fi
echo \n"------going to revision --------"\n
alembic revision --autogenerate -m "added a limit of 40 char for username column"

echo \n"Database revision complete."\n