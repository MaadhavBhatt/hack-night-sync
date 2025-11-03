import os
from datetime import datetime, timedelta, timezone
from supabase import create_client, Client

from .config import check_environment_variables, ENV_VARS_CHECKED, PLAN


TABLE_NAME = "hack_night_plans"
IS_INITIALIZED = False
CLIENT = None


def initialize_supabase() -> Client:
    """
    Initializes the Supabase client. Saves a global reference to the client.
    Checks if the required environment variables are set before initialization.
    """
    if not ENV_VARS_CHECKED:
        check_environment_variables()

    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(supabase_url, supabase_key)

    global IS_INITIALIZED, CLIENT
    IS_INITIALIZED = True
    CLIENT = supabase


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
        initialize_supabase()

    # Validate inputs
    if end_time is None and duration is not None:
        end_time = start_time + duration
    elif end_time is None and duration is None:
        raise ValueError("Either end_time or duration must be provided.")
    elif end_time is not None and duration is not None:
        raise ValueError("Only one of end_time or duration should be provided.")

    CLIENT.table(TABLE_NAME).insert(
        PLAN(
            user_id=user_id,
            plan=plan,
            start_time=str(start_time),
            end_time=str(end_time),
            created_at=str(created_at),
        )
    ).execute()


def get_plan_by_id(user_id: str, id: str) -> None:
    """
    Retrieves a Hack Night plan from the Supabase database by its ID.

    Args:
        user_id (str): The ID of the user retrieving the plan.
        id (str): The ID of the plan to be retrieved.
    """
    global IS_INITIALIZED
    if not IS_INITIALIZED:
        initialize_supabase()

    CLIENT.table(TABLE_NAME).select("*").eq("id", id).eq("user_id", user_id).execute()


def get_plans_by_user(
    user_id: str, count: int = -1, chronological: bool = False
) -> None:
    """
    Retrieves Hack Night plans for a specific user from the Supabase database.

    Args:
        user_id (str): The ID of the user whose plans are to be retrieved.
        count (int, optional): The number of plans to retrieve. Defaults to -1 (no limit).
        chronological (bool, optional): If True, retrieves plans in chronological order.
            Otherwise, retrieves in reverse chronological order. Defaults to False.
    """
    global IS_INITIALIZED
    if not IS_INITIALIZED:
        initialize_supabase()

    CLIENT.table(TABLE_NAME).select("*").eq("user_id", user_id).order(
        "created_at", desc=chronological is False
    ).limit(count).execute()


def get_plans_by_time(time: datetime) -> None:
    """
    Retrieves all Hack Night plans scheduled for a specific time from the Supabase database.

    Args:
        time (datetime): The time for which to retrieve plans.
    """
    global IS_INITIALIZED
    if not IS_INITIALIZED:
        initialize_supabase()

    CLIENT.table(TABLE_NAME).select("*").lte("start_time", str(time)).gte(
        "end_time", str(time)
    ).execute()


def cancel_plan_by_id(user_id: str, id: str) -> None:
    """
    Cancels a Hack Night plan in the Supabase database by its ID.

    Args:
        user_id (str): The ID of the user cancelling the plan.
        id (str): The ID of the plan to be cancelled.
    """
    global IS_INITIALIZED
    if not IS_INITIALIZED:
        initialize_supabase()

    CLIENT.table(TABLE_NAME).update({"cancelled": True}).eq("id", id).eq(
        "user_id", user_id
    ).execute()


def cancel_plans_by_user(user_id: str, latest: bool = True) -> None:
    """
    Cancels Hack Night plans for a specific user from the Supabase database.

    Args:
        user_id (str): The ID of the user whose plan is to be cancelled.
        latest (bool, optional): If True, cancels the latest plan. Defaults to True.
    """
    global IS_INITIALIZED
    if not IS_INITIALIZED:
        initialize_supabase()

    user_plans = get_plans_by_user(user_id)
    if not user_plans.data:
        return

    if latest:
        latest_plan = max(user_plans.data, key=lambda plan: plan["created_at"])
        cancel_plan_by_id(user_id, latest_plan["id"])
    else:
        for plan in user_plans.data:
            cancel_plan_by_id(user_id, plan["id"])
