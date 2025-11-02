import os
from dotenv import load_dotenv

ENV_VARS_CHECKED = False

CONFIG: dict = {}
COMMANDS = {
    "help": None,
    "me": "at",
    "cancel": None,
    "hello": None,
}

# Plan template
PLAN = lambda user_id, plan, created_at, start_time, end_time: {
    "user_id": user_id,
    "plan_title": plan,
    "created_at": created_at,
    "cancelled": False,
    "start_time": start_time,
    "end_time": end_time,
}

# Message templates
WELCOME_MESSAGE = lambda channel_name: [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"Hello! :wave: Welcome to the Hack Night Sync in *#{channel_name}* channel. Use `/hack-night help` to see the list of available commands.",
        },
    }
]
INVALID_COMMAND = lambda user_id: [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"Hello <@{user_id}>! :warning: The command you entered is invalid. Please use `/hack-night help` to see the list of valid commands.",
        },
    }
]
HELP_MESSAGE = lambda user_id: [
    {
        "type": "header",
        "text": {"type": "plain_text", "text": "Hack Night Sync - Help", "emoji": True},
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"Hello <@{user_id}>! Here are the available commands:",
        },
    },
    {
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": "`/hack-night help` - Display this help message\n",
            }
        ],
    },
]

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
