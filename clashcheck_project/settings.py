"""Settings and example data for ClashCheck."""


# Options shown in the interface.
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

LOCATIONS = [
    "City Campus",
    "Haymarket",
    "Moore Park",
    "Home",
    "Online",
]

# The example timetable used by the Load Example button.
EXAMPLE_EVENTS = [
    {
        "day": "Monday",
        "name": "Lecture",
        "start": "09:00",
        "end": "10:00",
        "location": "City Campus",
    },
    {
        "day": "Monday",
        "name": "Work shift",
        "start": "10:10",
        "end": "12:00",
        "location": "Haymarket",
    },
    {
        "day": "Tuesday",
        "name": "Tutorial",
        "start": "13:00",
        "end": "14:00",
        "location": "Moore Park",
    },
    {
        "day": "Tuesday",
        "name": "Study session",
        "start": "14:30",
        "end": "15:30",
        "location": "City Campus",
    },
]
