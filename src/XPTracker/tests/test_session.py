import time
import pytest
from unittest.mock import MagicMock
from XPTracker.core.session import GameSession
from XPTracker.core.input_receiver import InputReceiver


@pytest.fixture
def session():
    # We mock the receiver so we can manually control what "data" is waiting
    mock_receiver = MagicMock(spec=InputReceiver)
    sess = GameSession(mock_receiver)
    return sess, mock_receiver


def test_process_queue_calculates_xp(session):
    sess, mock_receiver = session

    # Setup the mock to return lines one by one, then None to stop the loop
    mock_receiver.remove_from_top.side_effect = [
        "You gain 1000 experience points.",
        "Garbage line with no XP.",
        "You gain 500 (+250) experience points.",
        None  # Stops the while loop
    ]

    # Run the processing
    logs = sess.process_queue()

    # Checks
    assert sess.total_xp == 1750, "Total XP calculation incorrect."
    assert len(logs) == 2, "Should return exactly 2 log entries (skipped garbage)."
    assert "1,000 XP" in logs[0]
    assert "750 XP" in logs[1]


def test_xp_per_hour_calculation(session):
    sess, _ = session

    # Fake a scenario: 10,000 XP gained in 30 minutes (1800 seconds)
    sess.total_xp = 10000
    sess.start_time = time.time() - 1800

    rate = sess.get_xp_per_hour()

    # 10k in half an hour = 20k/hr
    # Allow small margin of error for execution time
    assert 19000 < rate < 21000, f"Rate {rate} is outside expected range (~20000)."


def test_reset_clears_state(session):
    sess, _ = session
    sess.total_xp = 50000

    sess.reset()

    assert sess.total_xp == 0
    # Start time should be very close to "now"
    assert (time.time() - sess.start_time) < 1.0