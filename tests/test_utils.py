from datetime import datetime, timezone, timedelta
import pytest
from freezegun import freeze_time as freeze

from src.utils import is_past, is_recent


@freeze("2025-01-01T12:00:00Z")
def test_is_past_true_and_false():
    now = datetime.now(timezone.utc)
    assert is_past(now - timedelta(minutes=5)) is True
    assert is_past(now + timedelta(minutes=5)) is False


@freeze("2025-01-01T12:00:00Z")
def test_is_recent_within_and_outside_delta():
    now = datetime.now(timezone.utc)
    assert is_recent(now - timedelta(minutes=5), delta_minutes=10) is True
    assert is_recent(now + timedelta(minutes=5), delta_minutes=10) is True
    assert is_recent(now - timedelta(minutes=15), delta_minutes=10) is False
    assert is_recent(now + timedelta(minutes=15), delta_minutes=10) is False


def test_is_recent_naive_dt_raises():
    naive = datetime.now() - timedelta(minutes=5)
    with pytest.raises(ValueError):
        is_recent(naive, delta_minutes=10)


def test_is_recent_invalid_types_and_values():
    with pytest.raises(TypeError):
        is_recent("not a datetime", delta_minutes=10)
    with pytest.raises(TypeError):
        is_recent(datetime.now(timezone.utc), delta_minutes="ten")
    with pytest.raises(ValueError):
        is_recent(datetime.now(timezone.utc), delta_minutes=-5)
