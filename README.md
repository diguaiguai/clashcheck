# ClashCheck

**Creator: Tianqi Jiang**

ClashCheck is a desktop timetable prototype built with Python and Tkinter. It helps students check for overlapping events and insufficient travel time between events at different physical locations.

View the source code: **[Application interface](interface.py)** | **[Clash checking logic](clash_logic.py)** | **[Program entry point](main.py)**.

## Features

- Add events with a weekday, name, start time, end time and location.
- Display events in weekday and start-time order.
- Detect overlapping events on the same day.
- Check travel gaps using a configurable buffer from 0 to 120 minutes.
- Highlight conflicting events and explain each clash.
- Load example events, delete selected events or clear the timetable.

## Requirements

- Python 3 with Tkinter installed.
- A desktop environment to display the application window.

No third-party Python packages are required. To check that Tkinter is available, run:

```sh
python -m tkinter
```

If Tkinter is missing, install the Tkinter support provided by your Python distribution or operating system.

## Run the prototype

1. Download the repository using **Code > Download ZIP**, then extract it, or clone the repository.
2. Open a terminal in the extracted project folder containing `main.py`.
3. Run:

```sh
python main.py
```

On macOS or Linux, use `python3` instead of `python` if required by your installation.

## Try the example

1. Click **Load Example**.
2. Keep the default travel buffer of **20** minutes.
3. Click **Check Timetable**.

The Monday lecture ends at 10:00 at City Campus, and the work shift begins at 10:10 at Haymarket. ClashCheck flags the 10-minute gap because it is shorter than the required 20 minutes.

To enter your own events, choose a weekday and location, enter a name and 24-hour times such as `09:00` and `10:30`, then click **Add Event**. The end time must be later than the start time. Click **Check Timetable** to update the results after changing the timetable or travel buffer.

## How the checks work

Events overlap when their time ranges intersect on the same weekday. Back-to-back events do not overlap, but can still require travel time.

A travel warning appears when two non-overlapping events are at different physical locations and the gap is shorter than the selected buffer. Events marked **Online** do not require a travel buffer.

## Project files

| File | Purpose |
| --- | --- |
| [main.py](main.py) | Starts the application |
| [interface.py](interface.py) | Tkinter interface and user actions |
| [clash_logic.py](clash_logic.py) | Time conversion and clash detection |
| [settings.py](settings.py) | Weekdays, locations and example timetable |
| [test_logic.py](test_logic.py) | Unit tests for the checking logic |

## Tests

Run the existing unit tests from the project folder:

```sh
python -m unittest -v test_logic.py
```

The four tests cover time conversion, overlapping events, short travel gaps and a safe timetable.

## Current limitations

- Supports Monday to Friday and events within a single day.
- Uses fixed location options and one travel buffer for all locations.
- Does not use maps, routes or live traffic information.
- Stores events only while the application is open; closing it clears the timetable.
- Does not support saving, importing or exporting timetables.
- Runs locally as a desktop application. Download and run the source code to use it.
