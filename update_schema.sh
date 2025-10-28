#!/bin/bash

set -e

echo "WARNING: This script is not for production use. Do you wish to proceed? (y/n)"
read -r proceed
if [[ "$proceed" != "Y" && "$proceed" != "y" ]]; then
  echo "Aborting."
  exit 1
fi

if ! command -v supabase &> /dev/null; then
  echo "Error: supabase CLI is not installed. Please install it before running this script."
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

echo "Resetting the database (this will remove all data)..."
supabase db reset

echo "Applying the schema..."
supabase db push --file "$DB_DIR/schema.sql"

echo "Schemas successfully updated."
