"""Tkinter interface for ClashCheck."""

import tkinter as tk
from tkinter import messagebox, ttk

from clash_logic import find_clashes, time_to_minutes
from settings import DAYS, EXAMPLE_EVENTS, LOCATIONS


# The user's timetable is stored in this list.
events = []


def show_result(message):
    """Display a message in the result box."""
    result_text.config(state="normal")
    result_text.delete("1.0", tk.END)
    result_text.insert("1.0", message)
    result_text.config(state="disabled")


def refresh_table(clashing_rows=None):
    """Display all current events in the table."""
    if clashing_rows is None:
        clashing_rows = set()

    for row in event_table.get_children():
        event_table.delete(row)

    # Keep the original list number while sorting events for display.
    numbered_events = list(enumerate(events))
    numbered_events.sort(
        key=lambda item: (
            DAYS.index(item[1]["day"]),
            time_to_minutes(item[1]["start"]),
        )
    )

    for original_number, event in numbered_events:
        if original_number in clashing_rows:
            status = "CLASH"
            colour = "clash"
        else:
            status = "OK"
            colour = "normal"

        event_table.insert(
            "",
            tk.END,
            iid=str(original_number),
            values=(
                event["day"],
                event["name"],
                event["start"],
                event["end"],
                event["location"],
                status,
            ),
            tags=(colour,),
        )


def add_event():
    """Read the form and add one event."""
    name = name_entry.get().strip()
    start = start_entry.get().strip()
    end = end_entry.get().strip()

    if name == "":
        messagebox.showerror("Missing information", "Enter an event name.")
        return

    try:
        start_minutes = time_to_minutes(start)
        end_minutes = time_to_minutes(end)
    except ValueError as error:
        messagebox.showerror("Invalid time", str(error))
        return

    if start_minutes >= end_minutes:
        messagebox.showerror("Invalid time", "End time must be later than start time.")
        return

    new_event = {
        "day": day_box.get(),
        "name": name,
        "start": start,
        "end": end,
        "location": location_box.get(),
    }

    events.append(new_event)
    name_entry.delete(0, tk.END)
    refresh_table()
    show_result("Event added. Click Check Timetable when ready.")


def check_timetable():
    """Run the clash checker and show the result."""
    if len(events) == 0:
        messagebox.showinfo("Empty timetable", "Add at least one event first.")
        return

    try:
        travel_buffer = int(buffer_entry.get())
        if travel_buffer < 0 or travel_buffer > 120:
            raise ValueError
    except ValueError:
        messagebox.showerror(
            "Invalid travel buffer", "Enter a number between 0 and 120."
        )
        return

    messages, clashing_rows = find_clashes(events, travel_buffer)
    refresh_table(clashing_rows)

    if len(messages) == 0:
        show_result("No clashes found. The timetable is workable.")
    else:
        result = "Found " + str(len(messages)) + " clash(es):\n\n"
        result += "\n".join("• " + message for message in messages)
        show_result(result)


def delete_selected():
    """Delete the selected table rows."""
    selected_rows = event_table.selection()

    # Delete from the largest number so other list positions remain correct.
    row_numbers = sorted([int(row) for row in selected_rows], reverse=True)
    for row_number in row_numbers:
        del events[row_number]

    refresh_table()
    show_result("Selected event(s) deleted.")


def clear_all():
    """Delete every event after asking the user."""
    if len(events) == 0:
        return

    if messagebox.askyesno("Clear timetable", "Delete all events?"):
        events.clear()
        refresh_table()
        show_result("The timetable is empty.")


def load_example():
    """Copy the example events into the timetable."""
    events.clear()

    # copy() prevents changes to the original example data.
    for event in EXAMPLE_EVENTS:
        events.append(event.copy())

    refresh_table()
    show_result("Example loaded. Click Check Timetable to find the Monday clash.")


def create_input_form(parent):
    """Create the left side of the interface."""
    global day_box, name_entry, start_entry, end_entry
    global location_box, buffer_entry

    form = tk.LabelFrame(
        parent,
        text=" Add an Event ",
        bg="white",
        fg="#7e231f",
        font=("Arial", 14, "bold"),
        padx=15,
        pady=15,
    )
    form.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

    tk.Label(form, text="Day", bg="white").pack(anchor="w")
    day_box = ttk.Combobox(form, values=DAYS, state="readonly", width=23)
    day_box.set("Monday")
    day_box.pack(fill="x", pady=(3, 10))

    tk.Label(form, text="Event name", bg="white").pack(anchor="w")
    name_entry = ttk.Entry(form)
    name_entry.pack(fill="x", pady=(3, 10))

    tk.Label(form, text="Start time (HH:MM)", bg="white").pack(anchor="w")
    start_entry = ttk.Entry(form)
    start_entry.insert(0, "09:00")
    start_entry.pack(fill="x", pady=(3, 10))

    tk.Label(form, text="End time (HH:MM)", bg="white").pack(anchor="w")
    end_entry = ttk.Entry(form)
    end_entry.insert(0, "10:00")
    end_entry.pack(fill="x", pady=(3, 10))

    tk.Label(form, text="Location", bg="white").pack(anchor="w")
    location_box = ttk.Combobox(form, values=LOCATIONS, state="readonly")
    location_box.set("City Campus")
    location_box.pack(fill="x", pady=(3, 10))

    tk.Label(form, text="Travel buffer (minutes)", bg="white").pack(anchor="w")
    buffer_entry = ttk.Entry(form)
    buffer_entry.insert(0, "20")
    buffer_entry.pack(fill="x", pady=(3, 15))

    ttk.Button(form, text="Add Event", command=add_event).pack(fill="x")
    ttk.Button(form, text="Load Example", command=load_example).pack(
        fill="x", pady=(7, 0)
    )

    tk.Label(
        form,
        text="Fixed travel buffer only.\nNo maps or live traffic data.",
        bg="white",
        fg="#756762",
        justify="left",
        font=("Arial", 9),
    ).pack(anchor="w", pady=(18, 0))


def create_timetable(parent):
    """Create the table, buttons and result area."""
    global event_table, result_text

    timetable_frame = tk.LabelFrame(
        parent,
        text=" Weekly Timetable ",
        bg="white",
        fg="#7e231f",
        font=("Arial", 14, "bold"),
        padx=15,
        pady=15,
    )
    timetable_frame.grid(row=0, column=1, sticky="nsew")
    timetable_frame.columnconfigure(0, weight=1)
    timetable_frame.rowconfigure(0, weight=1)

    columns = ("day", "name", "start", "end", "location", "status")
    event_table = ttk.Treeview(timetable_frame, columns=columns, show="headings")

    headings = ["Day", "Event", "Start", "End", "Location", "Status"]
    widths = [90, 145, 60, 60, 115, 65]

    for column, title, width in zip(columns, headings, widths):
        event_table.heading(column, text=title)
        event_table.column(column, width=width)

    event_table.tag_configure("normal", background="white")
    event_table.tag_configure("clash", background="#f9d9d6", foreground="#7e231f")
    event_table.grid(row=0, column=0, sticky="nsew")

    button_row = tk.Frame(timetable_frame, bg="white")
    button_row.grid(row=1, column=0, sticky="ew", pady=10)

    ttk.Button(button_row, text="Delete Selected", command=delete_selected).pack(
        side="left"
    )
    ttk.Button(button_row, text="Clear All", command=clear_all).pack(
        side="left", padx=7
    )
    ttk.Button(button_row, text="Check Timetable", command=check_timetable).pack(
        side="right"
    )

    result_text = tk.Text(
        timetable_frame,
        height=7,
        bg="#faf7f5",
        fg="#302522",
        font=("Arial", 10),
        wrap="word",
    )
    result_text.grid(row=2, column=0, sticky="ew")
    show_result("Add events, then click Check Timetable.")


def create_window():
    """Build and return the complete program window."""
    root = tk.Tk()
    root.title("ClashCheck - Beginner Project")
    root.geometry("1000x650")
    root.minsize(850, 560)
    root.configure(bg="#f4f1ee")

    heading = tk.Frame(root, bg="#a8322d", height=90)
    heading.pack(fill="x")
    heading.pack_propagate(False)

    tk.Label(
        heading,
        text="ClashCheck",
        bg="#a8322d",
        fg="white",
        font=("Arial", 26, "bold"),
    ).pack(anchor="w", padx=25, pady=(14, 0))

    tk.Label(
        heading,
        text="Simple timetable and travel-time checker",
        bg="#a8322d",
        fg="#f7ddda",
        font=("Arial", 11),
    ).pack(anchor="w", padx=27)

    main_frame = tk.Frame(root, bg="#f4f1ee")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(0, weight=1)

    create_input_form(main_frame)
    create_timetable(main_frame)

    return root
