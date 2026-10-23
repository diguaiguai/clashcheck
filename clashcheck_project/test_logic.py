"""Simple tests for the ClashCheck logic."""

import unittest

from clash_logic import find_clashes, time_to_minutes


class ClashCheckTests(unittest.TestCase):
    def test_time_conversion(self):
        self.assertEqual(time_to_minutes("09:30"), 570)

    def test_time_overlap(self):
        events = [
            {
                "day": "Monday",
                "name": "Lecture",
                "start": "09:00",
                "end": "10:30",
                "location": "City Campus",
            },
            {
                "day": "Monday",
                "name": "Tutorial",
                "start": "10:00",
                "end": "11:00",
                "location": "City Campus",
            },
        ]

        messages, rows = find_clashes(events, 20)
        self.assertEqual(len(messages), 1)
        self.assertIn("overlaps", messages[0])
        self.assertEqual(rows, {0, 1})

    def test_travel_clash(self):
        events = [
            {
                "day": "Tuesday",
                "name": "Class",
                "start": "09:00",
                "end": "10:00",
                "location": "City Campus",
            },
            {
                "day": "Tuesday",
                "name": "Work",
                "start": "10:10",
                "end": "12:00",
                "location": "Haymarket",
            },
        ]

        messages, rows = find_clashes(events, 20)
        self.assertEqual(len(messages), 1)
        self.assertIn("20 minutes are required", messages[0])
        self.assertEqual(rows, {0, 1})

    def test_safe_timetable(self):
        events = [
            {
                "day": "Wednesday",
                "name": "Lecture",
                "start": "09:00",
                "end": "10:00",
                "location": "City Campus",
            },
            {
                "day": "Wednesday",
                "name": "Study",
                "start": "10:30",
                "end": "11:00",
                "location": "Haymarket",
            },
        ]

        messages, rows = find_clashes(events, 20)
        self.assertEqual(messages, [])
        self.assertEqual(rows, set())


if __name__ == "__main__":
    unittest.main()
