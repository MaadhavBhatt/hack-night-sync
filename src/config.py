import os
from dotenv import load_dotenv

ENV_VARS_CHECKED = False
CONFIG: dict = {}


load_dotenv()


def check_environment_variables() -> None:
    """
    Checks if the required environment variables are set for the application.
    Loads environment variables from a .env file if present.

    Raises:
        ValueError: If any of the required environment variables are not set or if the Firebase credentials file does not exist.

    This function checks for the following environment variables:
        - SLACK_BOT_TOKEN: The token for the Slack bot.
        - SLACK_APP_TOKEN: The token for the Slack app.
        - SUPABASE_URL: The URL for the Supabase instance.
        - SUPABASE_KEY: The API key for the Supabase instance.
    """
    global ENV_VARS_CHECKED
    if ENV_VARS_CHECKED:
        return

    required_vars = [
        "SLACK_BOT_TOKEN",
        "SLACK_APP_TOKEN",
        "SUPABASE_URL",
        "SUPABASE_KEY",
    ]

    optional_vars = []

    for var in required_vars:
        if os.environ.get(var) is None:
            raise ValueError(f"{var} environment variable is not set.")

    if optional_vars:
        global CONFIG
        for var in optional_vars:
            if os.environ.get(var) is None:
                os.environ[var] = "false"
                print(
                    f"Optional environment variable {var} is not set. Defaulting to false."
                )
            CONFIG[var.lower()] = os.environ.get(var).lower() == "true"

    ENV_VARS_CHECKED = True
