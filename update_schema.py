import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

SCHEMA_DIR = "./supabase/schema"
COMBINED_SCHEMA = "./supabase/schema.sql"


def combine_sql_files(schema_dir, combined_schema) -> None:
    if not os.path.isdir(schema_dir):
        raise FileNotFoundError(f"Schema directory '{schema_dir}' does not exist.")

    with open(combined_schema, "w") as outfile:
        for filename in os.listdir(schema_dir):
            if filename.endswith(".sql"):
                filepath = os.path.join(schema_dir, filename)
                with open(filepath, "r") as infile:
                    outfile.write(infile.read() + "\n\n")

    print(f"Combined SQL schema files into '{combined_schema}'.")


def apply_schema(combined_schema) -> None:
    try:
        connection = psycopg2.connect(
            user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DBNAME
        )
        connection.autocommit = True
        print("Connection successful!")

        with open(combined_schema, "r") as schema_file:
            schema_sql = schema_file.read()

        with connection.cursor() as cursor:
            cursor.execute(schema_sql)
            print("Database schema applied successfully.")

        connection.close()
        print("Connection closed.")

    except Exception as e:
        print(f"Failed to apply schema: {e}")


if __name__ == "__main__":
    print(
        "Warning: This script it not for production use. This will modify your database schema. Do you wish to proceed? (y/n)"
    )
    proceed = input().strip().lower()
    if proceed not in ["y", "yes"]:
        print("Aborting.")
        exit(1)

    try:
        combine_sql_files(SCHEMA_DIR, COMBINED_SCHEMA)
        apply_schema(COMBINED_SCHEMA)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
