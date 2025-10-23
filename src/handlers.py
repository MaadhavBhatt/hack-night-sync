from .config import COMMANDS, INVALID_COMMAND, WELCOME_MESSAGE, HELP_MESSAGE
from .slack_utils import send_ephemeral_message


def handle_hack_night_command(ack, body, client):
    ack()

    user_id = body.get("user_id", "unknown_user")
    channel_id = body.get("channel_id", "unknown_channel")
    thread_ts = body.get("thread_ts")
    text = body.get("text", "")

    parts = text.strip().lower().split()

    handle_command(parts, client, user_id, channel_id, thread_ts)


def handle_command(parts, client, user_id, channel_id, thread_ts):
    # If no command is provided, send the welcome message
    command = parts[0] if len(parts) > 0 else "hello"
    subcommand = parts[1] if len(parts) > 1 else ""

    # If the command or the subcommand is not valid, send an ephemeral message to the user
    if command not in COMMANDS or (subcommand and subcommand not in COMMANDS[command]):
        send_ephemeral_message(
            client,
            user_id,
            channel_id,
            blocks=INVALID_COMMAND(user_id),
            thread_ts=thread_ts,
        )
        return

    if command == "me":
        response = "me command received."
    elif command == "cancel":
        response = "Cancel command received."
    elif command == "help":
        response = HELP_MESSAGE(user_id)
    elif command == "hello":
        response = WELCOME_MESSAGE(channel_id)
    else:
        response = INVALID_COMMAND(user_id)

    send_ephemeral_message(
        client=client,
        user_id=user_id,
        channel_id=channel_id,
        blocks=response if isinstance(response, (dict, list)) else None,
        message=response if isinstance(response, str) else None,
        thread_ts=thread_ts,
    )
