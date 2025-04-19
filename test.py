import tkinter as tk

# Constants
WINDOW_HEIGHT = 500
STEP_SIZE = 50
GOAL_Y = 450
PATH_X_POSITIONS = {1: 150, 2: 350}

import random

# Set your configuration
num_levels = 2                   # Number of top-level keys (1, 2, etc.)
num_entries_per_level = 2       # Number of sub-entries per top-level key
value_range = (100, 450)        # Range for sub-dictionary keys
multiplier_range = (2, 5)       # Range for multiplier values

# Random multi gates
MULTIPLIERS = {
    level: {
        random.randint(*value_range): random.randint(*multiplier_range)
        for _ in range(num_entries_per_level)
    }
    for level in range(1, num_levels + 1)
}
print(MULTIPLIERS)


# Tkinter window 
root = tk.Tk()
root.title("brainrot sim")
root.geometry(f"500x{WINDOW_HEIGHT + 50}")

canvas = tk.Canvas(root, width=500, height=WINDOW_HEIGHT, bg="white")
canvas.pack()

# Draw vertical paths and finish lines
for path_id, x in PATH_X_POSITIONS.items():
    canvas.create_line(x, 10, x, GOAL_Y, width=4)
    canvas.create_line(x - 100, GOAL_Y, x + 100, GOAL_Y, fill="green", width=3)  # Finish line

# Draw multipliers
for path_id, m_dict in MULTIPLIERS.items():
    x = PATH_X_POSITIONS[path_id]
    for y, factor in m_dict.items():
        canvas.create_text(x - 30, y, text=f"x{factor}", font=("Arial", 14), fill="blue")

# State tracking
walkers = []
goal_count = 0

# UI: Score Display
score_label = tk.Label(root, text=f"People Reached Goal: {goal_count}", font=("Arial", 12))
score_label.pack()

# Reset walkers
def reset_walkers():
    global walkers, goal_count
    walkers.clear()
    canvas.delete("walker")
    goal_count = 0
    update_score()
    start_y = 10
    path_id = 1
    x = PATH_X_POSITIONS[path_id]
    walker_id = canvas.create_text(x, start_y, text="🚶", font=("Arial", 18), tags="walker")
    walkers.append({"id": walker_id, "path": path_id})

# Update score label
def update_score():
    score_label.config(text=f"People Reached Goal: {goal_count}")

# Move walkers
def walk():
    global goal_count
    new_walkers = []
    walkers_to_remove = []

    for walker in walkers:
        walker_id = walker["id"]
        path = walker["path"]
        canvas.move(walker_id, 0, STEP_SIZE)
        _, y = canvas.coords(walker_id)

        # Check for multipliers
        for m_y, factor in MULTIPLIERS[path].items():
            if abs(y - m_y) < STEP_SIZE // 2:
                for i in range(factor - 1):
                    new_x = PATH_X_POSITIONS[path] + (i + 1) * 10
                    clone = canvas.create_text(new_x, y, text="🚶", font=("Arial", 18), tags="walker")
                    new_walkers.append({"id": clone, "path": path})

        # Check for goal
        if y >= GOAL_Y:
            canvas.delete(walker_id)
            walkers_to_remove.append(walker)
            goal_count += 1
            update_score()

    # Remove walkers that reached the goal
    for w in walkers_to_remove:
        walkers.remove(w)

    walkers.extend(new_walkers)

# Switch path
def switch_paths():
    for walker in walkers:
        current_path = walker["path"]
        new_path = 2 if current_path == 1 else 1
        _, y = canvas.coords(walker["id"])
        new_x = PATH_X_POSITIONS[new_path]
        canvas.coords(walker["id"], new_x, y)
        walker["path"] = new_path

# UI Controls
control_frame = tk.Frame(root)
control_frame.pack(pady=10)

tk.Button(control_frame, text="Walk Down", command=walk).grid(row=0, column=0, padx=10)
tk.Button(control_frame, text="Switch Path", command=switch_paths).grid(row=0, column=1, padx=10)
tk.Button(control_frame, text="Reset", command=reset_walkers).grid(row=0, column=2, padx=10)

# Start
reset_walkers()

root.mainloop()
