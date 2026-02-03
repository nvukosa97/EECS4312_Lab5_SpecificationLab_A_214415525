## Student Name:
## Student ID: 

"""
Public test suite for the meeting slot suggestion exercise.

Students can run these tests locally to check basic correctness of their implementation.
The hidden test suite used for grading contains additional edge cases and will not be
available to students.
"""
import pytest
import sys
import os 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from solution import suggest_slots


def test_single_event_blocks_overlapping_slots():
    """
    Functional requirement:
    Slots overlapping an event must not be suggested.
    """
    events = [{"start": "10:00", "end": "11:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "10:00" not in slots
    assert "10:30" not in slots
    assert "11:15" in slots

def test_event_outside_working_hours_is_ignored():
    """
    Constraint:
    Events completely outside working hours should not affect availability.
    """
    events = [{"start": "07:00", "end": "08:00"}]
    slots = suggest_slots(events, meeting_duration=60, day="2026-02-01")

    assert "09:00" in slots
    assert "16:00" in slots

def test_unsorted_events_are_handled():
    """
    Constraint:
    Event order should not affect correctness.
    """
    events = [
        {"start": "13:00", "end": "14:00"},
        {"start": "09:30", "end": "10:00"},
        {"start": "11:00", "end": "12:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert  slots[1] == "10:15"
    assert "09:30" not in slots

def test_lunch_break_blocks_all_slots_during_lunch():
    """
    Constraint:
    No meeting may start during the lunch break (12:00–13:00).
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "12:00" not in slots
    assert "12:15" not in slots
    assert "12:30" not in slots
    assert "12:45" not in slots

"""TODO: Add at least 5 additional test cases to test your implementation."""

def test_event_ending_near_workday_end_blocks_late_slots():
    """
    Constraint:
    Meetings must fully fit within working hours.
    """
    events = [{"start": "16:00", "end": "16:30"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "16:30" not in slots
    assert "16:15" not in slots
    assert "15:30" in slots


def test_buffer_is_applied_after_event():
    """
    Constraint:
    A 15-minute buffer must be applied after an event.
    """
    events = [{"start": "09:00", "end": "10:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "10:00" not in slots
    assert "10:15" in slots


def test_overlapping_events_are_merged_correctly():
    """
    Constraint:
    Overlapping events should be treated as one continuous busy block.
    """
    events = [
        {"start": "10:00", "end": "11:00"},
        {"start": "10:30", "end": "11:30"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")
    print(slots)
    assert "11:00" not in slots
    assert "11:15" not in slots
    assert "12:00" not in slots
    assert "13:00" in slots


def test_meeting_exactly_fits_before_lunch():
    """
    Edge case:
    Meeting ending exactly at lunch start is allowed.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=60, day="2026-02-01")

    assert "11:00" in slots
    assert "11:15" not in slots  # would overlap lunch


def test_no_slots_when_meeting_duration_too_long():
    """
    Constraint:
    No slots should be returned if meeting duration exceeds any free interval.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=480, day="2026-02-01")

    assert slots == []

