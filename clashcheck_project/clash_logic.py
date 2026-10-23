"""Time conversion and clash checking functions."""


def time_to_minutes(time_text):
    """Convert a time such as 09:30 into minutes after midnight."""
    parts = time_text.split(":")

    if len(parts) != 2:
        raise ValueError("Use the HH:MM time format.")

    hour = int(parts[0])
    minute = int(parts[1])

    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        raise ValueError("Enter a valid 24-hour time.")

    return hour * 60 + minute


def find_clashes(events, travel_buffer):
    """Return conflict messages and the row numbers involved."""
    messages = []
    clashing_rows = set()

    # Use two loops to compare every pair of events.
    for first_number in range(len(events)):
        for second_number in range(first_number + 1, len(events)):
            first = events[first_number]
            second = events[second_number]

            # Events on different days cannot clash.
            if first["day"] != second["day"]:
                continue

            first_start = time_to_minutes(first["start"])
            first_end = time_to_minutes(first["end"])
            second_start = time_to_minutes(second["start"])
            second_end = time_to_minutes(second["end"])

            # Check whether the two time ranges overlap.
            if first_start < second_end and second_start < first_end:
                messages.append(
                    first["day"]
                    + ": "
                    + first["name"]
                    + " overlaps "
                    + second["name"]
                    + "."
                )
                clashing_rows.add(first_number)
                clashing_rows.add(second_number)
                continue

            # Find which event happens earlier.
            if first_start < second_start:
                earlier = first
                later = second
                earlier_number = first_number
                later_number = second_number
            else:
                earlier = second
                later = first
                earlier_number = second_number
                later_number = first_number

            gap = time_to_minutes(later["start"]) - time_to_minutes(earlier["end"])

            different_locations = earlier["location"] != later["location"]
            both_are_physical = (
                earlier["location"] != "Online" and later["location"] != "Online"
            )

            # Check whether the travel gap is too short.
            if different_locations and both_are_physical and gap < travel_buffer:
                messages.append(
                    earlier["day"]
                    + ": only "
                    + str(gap)
                    + " minutes between "
                    + earlier["name"]
                    + " and "
                    + later["name"]
                    + ". "
                    + str(travel_buffer)
                    + " minutes are required."
                )
                clashing_rows.add(earlier_number)
                clashing_rows.add(later_number)

    return messages, clashing_rows
