import os
from supabase import create_client, Client

from .config import check_environment_variables, ENV_VARS_CHECKED


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
    return supabase
