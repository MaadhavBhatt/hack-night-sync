import os
from datetime import datetime, timedelta, timezone
from supabase import create_client, Client

from .config import check_environment_variables, ENV_VARS_CHECKED, PLAN


TABLE_NAME = "hack-night-plans"
IS_INITIALIZED = False


def initialize_supabase() -> Client:
    """
    Initializes the Supabase client. Checks if the required environment variables are set before initialization.

    Returns:
        Client: A reference to the Supabase client.
    """
    if not ENV_VARS_CHECKED:
        check_environment_variables()

    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(supabase_url, supabase_key)

    global IS_INITIALIZED
    IS_INITIALIZED = True

    return supabase


def add_plan(
    user_id: str,
    plan: any,
    start_time: datetime,
    end_time: datetime = None,
    duration: timedelta = None,
    created_at: datetime = datetime.now(timezone.utc),
) -> None:
    """
    Adds a Hack Night plan to the Supabase database.

    Args:
        supabase (Client): The Supabase client.
        user_id (str): The ID of the user adding the plan.
        plan (any): The plan details to be added.
        start_time (datetime): The start time of the plan.
        end_time (datetime, optional): The end time of the plan. Defaults to None.
        duration (timedelta, optional): The duration of the plan. Defaults to None.
        created_at (datetime, optional): The creation time of the plan. Defaults to current UTC time.

    Raises:
        ValueError: If neither end_time nor duration is provided, or if both are provided.
    """
    # Initialize supabase if not already initialized
    global IS_INITIALIZED
    if not IS_INITIALIZED:
        supabase = initialize_supabase()

    # Validate inputs
    if end_time is None and duration is not None:
        end_time = start_time + duration
    elif end_time is None and duration is None:
        raise ValueError("Either end_time or duration must be provided.")
    elif end_time is not None and duration is not None:
        raise ValueError("Only one of end_time or duration should be provided.")

    supabase.table(TABLE_NAME).insert(
        PLAN(
            user_id=user_id,
            plan=plan,
            start_time=str(start_time),
            end_time=str(end_time),
            created_at=str(created_at),
        )
    ).execute()
