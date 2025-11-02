#!/bin/bash

set -e

echo "WARNING: This script is not for production use. Do you wish to proceed? (y/n)"
read -r proceed
if [[ "$proceed" != "Y" && "$proceed" != "y" ]]; then
  echo "Aborting."
  exit 1
fi

if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
else
  echo "Error: .env file not found."
  exit 1
fi

SCHEMA_DIR="./schema"
DB_DIR="./supabase"
COMBINED_SCHEMA="$DB_DIR/schema.sql"

echo "Starting schema update..."

if [ -d "$DB_DIR/$SCHEMA_DIR" ]; then
  cat "$DB_DIR/$SCHEMA_DIR"/*.sql > "$COMBINED_SCHEMA"
  echo "Combined schema files into $COMBINED_SCHEMA"
else
  echo "Error: Schema directory $DB_DIR/$SCHEMA_DIR does not exist."
  exit 1
fi

echo "Applying the schema..."
psql "$DB_URL" -f "$COMBINED_SCHEMA"

echo "Schemas successfully updated."
