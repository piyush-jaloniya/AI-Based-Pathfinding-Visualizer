import tkinter as tk
from tkinter import messagebox
import random
from algorithms.astar import a_star
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.bestfs import best_first_search
from algorithms.hill_climbing import hill_climbing

ROWS, COLS = 20, 20  # Grid size
grid = [[0] * COLS for _ in range(ROWS)]  # Initialize grid (0 = free, 1 = obstacle)

start, end = None, None
selected_algorithm = None
grid_elements = {}  # Store rectangle references

def draw_grid():
    """Draws the grid with updated colors for obstacles, start, end, and paths."""
    global grid_elements
    canvas.delete("all")
    grid_elements = {}
    for r in range(ROWS):
        for c in range(COLS):
            color = "white"
            if grid[r][c] == 1:
                color = "black"
            elif (r, c) == start:
                color = "green"
            elif (r, c) == end:
                color = "red"
            rect = canvas.create_rectangle(
                c * 30, r * 30, (c + 1) * 30, (r + 1) * 30, fill=color, outline="gray"
            )
            grid_elements[(r, c)] = rect

def set_cell(event):
    """Handles cell clicks to set Start, End, or Obstacles."""
    global start, end
    row, col = event.y // 30, event.x // 30
    if 0 <= row < ROWS and 0 <= col < COLS:
        if (row, col) == start:
            start = None
        elif (row, col) == end:
            end = None
        elif start is None:
            start = (row, col)
        elif end is None:
            end = (row, col)
        else:
            grid[row][col] = 1 - grid[row][col]  # Toggle obstacle
    draw_grid()

def run_algorithm():
    """Runs the selected algorithm and visualizes the path."""
    global start, end
    if not start or not end:
        status_label.config(text="Set Start and End points first!", fg="red")
        return

    algorithms = {
        "A*": a_star,
        "BFS": bfs,
        "DFS": dfs,
        "Best-First": best_first_search,
        "Hill Climbing": hill_climbing
    }

    if selected_algorithm in algorithms:
        path = algorithms[selected_algorithm](grid, start, end)
        if path:
            for r, c in path:
                if (r, c) != end:  # Keep goal node red
                    canvas.itemconfig(grid_elements[(r, c)], fill="yellow")
            status_label.config(text=f"{selected_algorithm} found a path!", fg="green")
        else:
            status_label.config(text="No path found!", fg="red")
    else:
        status_label.config(text="Select an algorithm!", fg="red")

def select_algorithm(algo):
    """Updates the selected algorithm from dropdown."""
    global selected_algorithm
    selected_algorithm = algo
    status_label.config(text=f"Selected: {algo}", fg="blue")

def reset():
    """Resets the grid and clears all selections."""
    global grid, start, end, selected_algorithm
    grid = [[0] * COLS for _ in range(ROWS)]
    start = end = None
    selected_algorithm_var.set("Select Algorithm")
    selected_algorithm = None
    status_label.config(text="Select an algorithm and set points", fg="black")
    draw_grid()

def add_random_obstacles():
    """Adds random obstacles while keeping start and end clear."""
    global grid
    obstacle_density = 0.3  # 30% of grid will be obstacles
    for r in range(ROWS):
        for c in range(COLS):
            if (r, c) != start and (r, c) != end:  # Keep start and end clear
                grid[r][c] = 1 if random.random() < obstacle_density else 0
    draw_grid()

# 💡 Help Message
def show_help():
    help_text = """How to Use This App:
1. Click on any cell to set the **Start** point (Green).
2. Click on another cell to set the **End** point (Red).
3. Click on additional cells to **add obstacles** (Black).
4. Select an algorithm from the dropdown menu.
5. Click 'Run' to visualize the path (Yellow).
6. Click 'Random Obstacles' to fill the grid randomly.
7. Press 'Reset' to clear the grid.
"""
    messagebox.showinfo("Help", help_text)

# ℹ️ About Message
def show_about():
    about_text = """Pathfinding Visualizer
Version: 1.0
This application helps visualize different pathfinding algorithms:
- A* Search
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Best-First Search
- Hill Climbing

Developed using Python and Tkinter.
"""
    messagebox.showinfo("About", about_text)

def customize_grid():
    """Opens a dialog to set custom grid size."""
    custom_window = tk.Toplevel(root)
    custom_window.title("Customize Grid")

    tk.Label(custom_window, text="Rows:").grid(row=0, column=0)
    row_entry = tk.Entry(custom_window)
    row_entry.grid(row=0, column=1)
    row_entry.insert(0, str(ROWS))  # Default value

    tk.Label(custom_window, text="Columns:").grid(row=1, column=0)
    col_entry = tk.Entry(custom_window)
    col_entry.grid(row=1, column=1)
    col_entry.insert(0, str(COLS))  # Default value

    def apply_changes():
        """Applies new grid size and redraws the grid."""
        global ROWS, COLS, grid, start, end
        try:
            new_rows = int(row_entry.get())
            new_cols = int(col_entry.get())

            if new_rows < 5 or new_cols < 5:  # Prevents too small grids
                messagebox.showwarning("Warning", "Grid size must be at least 5x5!")
                return

            ROWS, COLS = new_rows, new_cols
            grid = [[0] * COLS for _ in range(ROWS)]  # Reset grid
            start = end = None  # Reset start & end points
            canvas.config(width=COLS * 30, height=ROWS * 30)  # Resize canvas
            draw_grid()
            custom_window.destroy()

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")

    tk.Button(custom_window, text="Apply", command=apply_changes, bg="green").grid(row=2, columnspan=2)



# 🖥️ Create the main window
root = tk.Tk()
root.title("Pathfinding Visualizer")

# 📌 Menu Bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# 📌 Add Help and About to Menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Help", command=show_help)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)

# 🖼️ Create the grid canvas
canvas = tk.Canvas(root, width=COLS * 30, height=ROWS * 30, bg="white")
canvas.pack()
canvas.bind("<Button-1>", set_cell)

# 🎛️ Control Panel
button_frame = tk.Frame(root)
button_frame.pack()

# 📌 Dropdown Menu for Algorithm Selection
selected_algorithm_var = tk.StringVar()
selected_algorithm_var.set("Select Algorithm")  # Default text
algorithm_menu = tk.OptionMenu(button_frame, selected_algorithm_var, "A*", "BFS", "DFS", "Best-First", "Hill Climbing", command=select_algorithm)
algorithm_menu.config(bg="lightgrey", fg="black" )
algorithm_menu.pack(side=tk.LEFT)

# 🏃 Run and Reset Buttons
tk.Button(button_frame, text="Run", command=run_algorithm, bg="grey").pack(side=tk.LEFT)
tk.Button(button_frame, text="Reset", command=reset, bg="grey").pack(side=tk.LEFT)
tk.Button(button_frame, text="Random Obstacles", command=add_random_obstacles, bg="grey").pack(side=tk.LEFT)
# Add "Customize Grid" button to UI
tk.Button(button_frame, text="Customize Grid", command=customize_grid, bg="purple", fg="white").pack(side=tk.LEFT)


# 🔹 Status Label
status_label = tk.Label(root, text="Select an algorithm and set points", fg="black")
status_label.pack()

# 🖌️ Draw initial grid
draw_grid()

# 🔄 Start the Tkinter event loop
root.mainloop()
