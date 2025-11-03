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


# Plan template
class Plan:
    def __init__(
        self,
        id: str,
        slack_user_id: str,
        plan_title: str,
        created_at: str,
        start_time: str,
        end_time: str,
        cancelled: bool = False,
        **kwargs,
    ):
        self.id = id
        self.slack_user_id = slack_user_id
        self.plan_title = plan_title
        self.created_at = created_at
        self.start_time = start_time
        self.end_time = end_time
        self.cancelled = cancelled

        self.options = kwargs

    def to_dict(self):
        return {
            "id": self.id,
            "slack_user_id": self.slack_user_id,
            "plan_title": self.plan_title,
            "created_at": self.created_at,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "cancelled": self.cancelled,
            **self.options,
        }

    def __repr__(self):
        return f"Plan at ID {self.id} for user {self.slack_user_id} titled '{self.plan_title}'"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if not isinstance(other, Plan):
            return False
        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        return not self.__eq__(other)


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
