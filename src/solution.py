## Student Name: Noah Vukosa
## Student ID: 214415525

"""
Stub file for the meeting slot suggestion exercise.

Implement the function `suggest_slots` to return a list of valid meeting start times
on a given day, taking into account working hours, and possible specific constraints. See the lab handout
for full requirements.
"""
from typing import List, Dict
from datetime import datetime

def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:

    def to_minutes(t: str) -> int:
        h, m = map(int, t.split(":"))
        return h * 60 + m

    def to_time_str(m: int) -> str:
        return f"{m // 60:02d}:{m % 60:02d}"

    WORK_START = to_minutes("09:00")
    WORK_END = to_minutes("17:00")
    LUNCH_START = to_minutes("12:00")
    LUNCH_END = to_minutes("13:00")
    BUFFER = 15
    SLOT_STEP = 15

    # Friday rule: no meeting may START at or after 15:00
    is_friday = datetime.strptime(day, "%Y-%m-%d").weekday() == 4  # Mon=0 ... Fri=4
    FRIDAY_CUTOFF = to_minutes("15:00")

    # Convert events to minutes and sort
    busy = [(to_minutes(e["start"]), to_minutes(e["end"])) for e in events]
    busy.sort()

    # Merge overlapping events
    merged = []
    for s, e in busy:
        if not merged or s > merged[-1][1]:
            merged.append([s, e])
        else:
            merged[-1][1] = max(merged[-1][1], e)

    # Build free intervals (without buffer here)
    free = []
    current = WORK_START
    for s, e in merged:
        if s > current:
            free.append((current, s))
        current = max(current, e)  # buffer handled when checking slots
    if current < WORK_END:
        free.append((current, WORK_END))

    slots = []
    for start, end in free:
        t = ((start + SLOT_STEP - 1) // SLOT_STEP) * SLOT_STEP  # align to 15-min
        while t + meeting_duration <= end:
            # Enforce Friday cutoff on start time
            if is_friday and t >= FRIDAY_CUTOFF:
                break  # later times will also be >= cutoff in this interval

            # Check if this slot overlaps any event including buffer
            conflict = False
            for s, e in merged:
                if t < e + BUFFER and t + meeting_duration > s:
                    conflict = True
                    break

            # Check lunch
            if t < LUNCH_START and t + meeting_duration > LUNCH_START:
                conflict = True
            if t >= LUNCH_START and t < LUNCH_END:
                conflict = True

            if not conflict:
                slots.append(to_time_str(t))
            t += SLOT_STEP

    return slots

