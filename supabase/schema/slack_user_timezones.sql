CREATE TABLE public.slack_user_timezones (
  id SERIAL PRIMARY KEY,
  slack_user_id TEXT NOT NULL UNIQUE,
  timezone TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
