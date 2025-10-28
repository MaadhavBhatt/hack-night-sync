from typing import Union
from slack_sdk import WebClient


def create_message_blocks(message=None, blocks=None):
    """
    Creates a list of message blocks for Slack messages.
    If both 'message' and 'blocks' are provided, it raises a ValueError.
    If neither is provided, it raises a ValueError.

    Args:
        message (str): The message text to include in the blocks.
        blocks (list): A list of blocks to include in the message.

    Returns:
        list: A list of blocks to be used in a Slack message.
    """
    if message and blocks:
        raise ValueError("Either 'message' or 'blocks' must be provided, but not both.")
    elif not message and not blocks:
        raise ValueError(
            "Either 'message' or 'blocks' must be provided. Both cannot be empty."
        )

    if blocks is None:
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{message}",
                },
            }
        ]
    elif isinstance(blocks, dict):
        blocks = [blocks]

    return blocks


def send_ephemeral_message(
    client, user_id, channel_id, blocks=None, message=None, thread_ts=None
):
    """
    Sends an ephemeral message visible only to the specified user in a Slack channel.

    An ephemeral message is visible only to the user specified and not to other users
    in the channel.

    Args:
        client: The Slack client instance used to send the message.
        user_id (str): The ID of the user who will see the ephemeral message.
        channel_id (str): The ID of the channel where the message is sent.
        blocks (list, optional): Predefined blocks for structured message content.
            If not provided but message is, blocks will be created from the message.
        message (str, optional): Text content of the message.
        thread_ts (str, optional): Timestamp of the thread to send the message in.
            If omitted, the message will not be sent in a thread.

    Returns:
        None
    """
    blocks = create_message_blocks(message, blocks)
    client.chat_postEphemeral(
        user=user_id,
        channel=channel_id,
        thread_ts=thread_ts,
        blocks=blocks,
        text=f"{message}",
    )


def send_channel_message(client, channel_id, blocks=None, message=None, thread_ts=None):
    """
    Sends a message to a Slack channel.

    Args:
        client: The Slack client instance used to send the message.
        channel_id (str): The ID of the channel where the message is sent.
        blocks (list, optional): Predefined blocks for structured message content.
            If not provided but message is, blocks will be created from the message.
        message (str, optional): Text content of the message.
        thread_ts (str, optional): Timestamp of the thread to send the message in.
            If omitted, the message will not be sent in a thread.

    Returns:
        None
    """
    blocks = create_message_blocks(message, blocks)
    client.chat_postMessage(
        channel=channel_id,
        thread_ts=thread_ts,
        blocks=blocks,
        text=f"{message}",
    )


def get_timezone_from_user_id(
    user_id: str,
    client: WebClient,
    get_only_offset: bool = False,
    get_only_label: bool = False,
) -> Union[dict, str, int]:
    """
    Retrieves the timezone of a Slack user based on their user ID.

    Args:
        user_id (str): The Slack user ID.
        client: The Slack client instance used to fetch user information.
        get_only_offset (bool, optional): Whether to only return the timezone offset. Defaults to False.
        get_only_label (bool, optional): Whether to only return the timezone label. Defaults to False.

    Returns:
        Union[dict, str, int]: A dictionary with timezone information, or just the offset or label if specified.

    Raises:
        ValueError: If both get_only_offset and get_only_label are set to True.
        ValueError: If the user information cannot be retrieved or if the requested timezone information is unavailable
    """
    if get_only_offset and get_only_label:
        raise ValueError("Cannot set both get_only_offset and get_only_label to True.")

    user_info = client.users_info(user=user_id)
    if not user_info["ok"]:
        raise ValueError(f"Could not retrieve user info for user ID: {user_id}")

    user = user_info.get("user")
    timezone = user.get("tz")
    timezone_label = user.get("tz_label")
    timezone_offset = user.get("tz_offset")

    if get_only_offset:
        if timezone_offset is None:
            raise ValueError(f"Timezone offset not available for user ID: {user_id}")
        return timezone_offset

    if get_only_label:
        if timezone_label is None:
            raise ValueError(f"Timezone label not available for user ID: {user_id}")
        return timezone_label

    if not all([timezone, timezone_label, timezone_offset]):
        raise ValueError(
            f"Timezone information incomplete for user ID: {user_id}\n"
            f"timezone is {timezone}\n"
            f"timezone_label is {timezone_label}\n"
            f"timezone_offset is {timezone_offset}\n"
        )

    return {
        "timezone": timezone,
        "timezone_label": timezone_label,
        "timezone_offset": timezone_offset,
    }
