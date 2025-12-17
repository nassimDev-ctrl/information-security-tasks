import tkinter as tk
from tkinter import messagebox
import heapq
ROWS = 10
COLS = 15
CELL_SIZE = 40

EMPTY = 0
WALL = 1
FIRE = 2
EXIT = 3
PERSON = 4
PATH = 5

COLORS = {
    EMPTY: "#ffffff",
    WALL: "#2c3e50",
    FIRE: "#e74c3c",
    EXIT: "#27ae60",
    PERSON: "#3498db",
    PATH: "#f39c12"
}

# Enhanced color scheme
BG_COLOR = "#f5f6fa"
PANEL_BG = "#ffffff"
ACCENT_COLOR = "#2c3e50"
SUCCESS_COLOR = "#27ae60"
WARNING_COLOR = "#f39c12"
DANGER_COLOR = "#e74c3c"
INFO_COLOR = "#3498db"
BORDER_COLOR = "#d5d8dc"
TEXT_SECONDARY = "#7f8c8d"
SHADOW_COLOR = "#bdc3c7"
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
def astar(grid, start, goals):
    rows = len(grid)
    cols = len(grid[0])

    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current in goals:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = current[0] + dx, current[1] + dy

            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] in (WALL, FIRE):
                    continue

                neighbor = (nr, nc)
                tentative_g = g_score[current] + 1

                if tentative_g < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + min(
                        heuristic(neighbor, g) for g in goals
                    )
                    heapq.heappush(open_set, (f_score, neighbor))

    return None
class EvacuationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚨 Emergency Evacuation System - A* Pathfinding")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.current_mode = WALL
        self.mode_buttons = {}  

        self.create_layout()
        self.draw_grid()
        
        if WALL in self.mode_buttons:
            self.set_mode(WALL)
        self.load_initial_scenario()
        self.update_grid_status()


    def create_layout(self):
        main_container = tk.Frame(self.root, bg=BG_COLOR, padx=25, pady=25)
        main_container.pack(fill=tk.BOTH, expand=True)

        left_frame = tk.Frame(
            main_container, 
            bg=PANEL_BG, 
            relief=tk.FLAT,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1
        )
        left_frame.pack(side=tk.LEFT, padx=(0, 20), pady=10)

        header_frame = tk.Frame(left_frame, bg=PANEL_BG)
        header_frame.pack(fill=tk.X, pady=(20, 15), padx=20)

        title = tk.Label(
            header_frame,
            text="🗺️ Building Evacuation Map",
            font=("Segoe UI", 20, "bold"),
            bg=PANEL_BG,
            fg=ACCENT_COLOR
        )
        title.pack()

        subtitle = tk.Label(
            header_frame,
            text="Click or drag on the grid to place elements",
            font=("Segoe UI", 10),
            bg=PANEL_BG,
            fg=TEXT_SECONDARY
        )
        subtitle.pack(pady=(5, 0))

        divider = tk.Frame(header_frame, bg=BORDER_COLOR, height=1)
        divider.pack(fill=tk.X, pady=(12, 0))

        canvas_frame = tk.Frame(left_frame, bg=PANEL_BG, padx=20, pady=20)
        canvas_frame.pack()

        self.canvas = tk.Canvas(
            canvas_frame,
            width=COLS * CELL_SIZE + 4,
            height=ROWS * CELL_SIZE + 4,
            bg="#e0e0e0",
            highlightthickness=3,
            highlightbackground="#b0b0b0",
            highlightcolor="#b0b0b0",
            relief=tk.FLAT,
            cursor="crosshair"
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<B1-Motion>", self.handle_click)  # Allow dragging

        right_frame = tk.Frame(
            main_container, 
            bg=PANEL_BG, 
            relief=tk.FLAT,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
            width=280
        )
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(20, 0), pady=10)
        right_frame.pack_propagate(False)

        self.create_controls(right_frame)

    def create_controls(self, parent):
        # Header with divider
        header_frame = tk.Frame(parent, bg=PANEL_BG)
        header_frame.pack(fill=tk.X, pady=(20, 15), padx=20)

        header = tk.Label(
            header_frame,
            text="⚙️ Control Panel",
            font=("Segoe UI", 18, "bold"),
            bg=PANEL_BG,
            fg=ACCENT_COLOR
        )
        header.pack()

        divider1 = tk.Frame(header_frame, bg=BORDER_COLOR, height=1)
        divider1.pack(fill=tk.X, pady=(12, 0))

        # Mode selection section
        mode_label = tk.Label(
            parent,
            text="Select Mode:",
            font=("Segoe UI", 11, "bold"),
            bg=PANEL_BG,
            fg=ACCENT_COLOR,
            anchor="w"
        )
        mode_label.pack(fill=tk.X, padx=20, pady=(15, 10))

        # Mode buttons with icons
        modes_frame = tk.Frame(parent, bg=PANEL_BG)
        modes_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        self.create_button(modes_frame, "🧱 Wall", WALL, COLORS[WALL], "#1a252f")
        self.create_button(modes_frame, "🔥 Fire", FIRE, COLORS[FIRE], "#c0392b")
        self.create_button(modes_frame, "🚪 Exit", EXIT, COLORS[EXIT], "#229954")
        self.create_button(modes_frame, "👤 Person", PERSON, COLORS[PERSON], "#2980b9")
        self.create_button(modes_frame, "🧹 Clear", EMPTY, "#95a5a6", "#7f8c8d")

        # Action buttons section
        action_label = tk.Label(
            parent,
            text="Actions:",
            font=("Segoe UI", 11, "bold"),
            bg=PANEL_BG,
            fg=ACCENT_COLOR,
            anchor="w"
        )
        action_label.pack(fill=tk.X, padx=20, pady=(10, 10))

        actions_frame = tk.Frame(parent, bg=PANEL_BG)
        actions_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        # Start Evacuation button with enhanced styling
        self.start_btn = tk.Button(
            actions_frame,
            text="▶️ Start Evacuation",
            bg=SUCCESS_COLOR,
            fg="white",
            font=("Segoe UI", 12, "bold"),
            command=self.start_evacuation,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=15,
            pady=10,
            activebackground="#229954",
            activeforeground="white"
        )
        self.start_btn.pack(fill=tk.X, pady=(0, 10))
        self.start_btn.bind("<Enter>", lambda e: self.start_btn.config(bg="#229954", relief=tk.RAISED))
        self.start_btn.bind("<Leave>", lambda e: self.start_btn.config(bg=SUCCESS_COLOR, relief=tk.FLAT))

        # Reset button
        reset_btn = tk.Button(
            actions_frame,
            text="🔄 Reset Grid",
            bg="#95a5a6",
            fg="white",
            font=("Segoe UI", 11),
            command=self.reset_grid,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=15,
            pady=8,
            activebackground="#7f8c8d",
            activeforeground="white"
        )
        reset_btn.pack(fill=tk.X)
        reset_btn.bind("<Enter>", lambda e: reset_btn.config(bg="#7f8c8d", relief=tk.RAISED))
        reset_btn.bind("<Leave>", lambda e: reset_btn.config(bg="#95a5a6", relief=tk.FLAT))

        # Status section with enhanced styling
        status_frame = tk.Frame(
            parent, 
            bg="#f8f9fa", 
            relief=tk.FLAT,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1
        )
        status_frame.pack(fill=tk.X, padx=20, pady=(0, 15))

        status_title = tk.Label(
            status_frame,
            text="📊 Status",
            font=("Segoe UI", 11, "bold"),
            bg="#f8f9fa",
            fg=ACCENT_COLOR
        )
        status_title.pack(pady=(12, 8))

        self.status = tk.Label(
            status_frame,
            text="Ready to build map",
            font=("Segoe UI", 10),
            bg="#f8f9fa",
            fg=ACCENT_COLOR,
            wraplength=220,
            justify=tk.LEFT
        )
        self.status.pack(pady=(0, 12), padx=12)

        # Legend section with enhanced styling
        legend_frame = tk.Frame(
            parent, 
            bg="#f8f9fa", 
            relief=tk.FLAT,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1
        )
        legend_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        legend_title = tk.Label(
            legend_frame,
            text="📋 Legend",
            font=("Segoe UI", 11, "bold"),
            bg="#f8f9fa",
            fg=ACCENT_COLOR
        )
        legend_title.pack(pady=(12, 10))

        legend_items = [
            ("🧱 Wall", COLORS[WALL]),
            ("🔥 Fire", COLORS[FIRE]),
            ("🚪 Exit", COLORS[EXIT]),
            ("👤 Person", COLORS[PERSON]),
            ("🟡 Path", COLORS[PATH])
        ]

        for text, color in legend_items:
            item_frame = tk.Frame(legend_frame, bg="#f8f9fa")
            item_frame.pack(fill=tk.X, padx=12, pady=3)
            
            color_box = tk.Label(
                item_frame,
                text="  ",
                bg=color,
                width=4,
                relief=tk.RAISED,
                bd=1,
                height=1
            )
            color_box.pack(side=tk.LEFT, padx=(0, 10))
            
            tk.Label(
                item_frame,
                text=text,
                font=("Segoe UI", 9),
                bg="#f8f9fa",
                fg=ACCENT_COLOR
            ).pack(side=tk.LEFT)
        
        tk.Label(legend_frame, bg="#f8f9fa").pack(pady=8)

    def create_button(self, parent, text, mode, color, hover_color=None):
        if hover_color is None:
            hover_color = color
        
        btn = tk.Button(
            parent,
            text=text,
            bg=color,
            fg="white",
            font=("Segoe UI", 11, "bold"),
            command=lambda: self.set_mode(mode),
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=12,
            pady=8,
            activebackground=hover_color,
            activeforeground="white"
        )
        btn.pack(fill="x", pady=4)
        
        # Store button reference
        self.mode_buttons[mode] = btn
        
        # Enhanced hover effects
        def on_enter(e, btn=btn, hover=hover_color):
            btn.config(bg=hover, relief=tk.RAISED)
        
        def on_leave(e, btn=btn, original=color):
            btn.config(bg=original, relief=tk.FLAT)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def set_mode(self, mode):
        self.current_mode = mode
        mode_names = {
            WALL: "Wall", 
            FIRE: "Fire", 
            EXIT: "Exit", 
            PERSON: "Person", 
            EMPTY: "Clear"
        }
        
        # Visual feedback: highlight selected button
        for m, btn in self.mode_buttons.items():
            if m == mode:
                btn.config(relief=tk.SUNKEN, bd=2)
            else:
                btn.config(relief=tk.FLAT, bd=0)
        
        mode_name = mode_names.get(mode, 'Unknown')
        self.status.config(text=f"✓ Mode: {mode_name}")
    def handle_click(self, event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE

        if 0 <= row < ROWS and 0 <= col < COLS:
            self.grid[row][col] = self.current_mode
            self.draw_grid()
            
            # Update status with grid readiness
            self.update_grid_status()
    
    def update_grid_status(self):
        validation = self.validate_grid()
        
        if not validation['valid']:
            missing = ", ".join(validation['errors'])
            self.status.config(text=f"⚠️ Missing: {missing}")
        elif validation['has_person'] and validation['has_exit']:
            self.status.config(text=f"✓ Ready! Person: {validation['person_count']}, Exits: {validation['exit_count']}")
        else:
            self.status.config(text="Ready to build map")
    def draw_grid(self):
        self.canvas.delete("all")

        for r in range(ROWS):
            for c in range(COLS):
                x = c * CELL_SIZE
                y = r * CELL_SIZE
                cell = self.grid[r][c]

                # ممرات (أرضية)
                if cell == EMPTY:
                    self.canvas.create_rectangle(
                        x, y,
                        x + CELL_SIZE, y + CELL_SIZE,
                        fill="#ecf0f1",
                        outline="#bdc3c7"
                    )

                # جدران (سميكة)
                elif cell == WALL:
                    self.canvas.create_rectangle(
                        x, y,
                        x + CELL_SIZE, y + CELL_SIZE,
                        fill=COLORS[WALL],
                        outline=COLORS[WALL]
                    )

                # مخرج (باب)
                elif cell == EXIT:
                    self.canvas.create_rectangle(
                        x + 6, y + 6,
                        x + CELL_SIZE - 6, y + CELL_SIZE - 6,
                        fill=COLORS[EXIT],
                        outline="#145a32",
                        width=3
                    )
                    self.canvas.create_text(
                        x + CELL_SIZE//2,
                        y + CELL_SIZE - 10,
                        text="EXIT",
                        fill="white",
                        font=("Segoe UI", 8, "bold")
                    )

                # شخص (دائرة)
                elif cell == PERSON:
                    self.canvas.create_oval(
                        x + 6, y + 6,
                        x + CELL_SIZE - 6, y + CELL_SIZE - 6,
                        fill=COLORS[PERSON],
                        outline="#154360",
                        width=2
                    )

                # حريق
                elif cell == FIRE:
                    self.canvas.create_rectangle(
                        x, y,
                        x + CELL_SIZE, y + CELL_SIZE,
                        fill=COLORS[FIRE],
                        outline="#922b21"
                    )
                    self.canvas.create_text(
                        x + CELL_SIZE//2,
                        y + CELL_SIZE//2,
                        text="🔥",
                        font=("Segoe UI", 14)
                    )

                # مسار الإخلاء
                elif cell == PATH:
                    self.canvas.create_rectangle(
                        x + 2, y + 2,
                        x + CELL_SIZE - 2, y + CELL_SIZE - 2,
                        fill=COLORS[PATH],
                        outline="#d68910",
                        width=2
                    )
                    # Draw arrow indicator
                    self.canvas.create_text(
                        x + CELL_SIZE//2,
                        y + CELL_SIZE//2,
                        text="→",
                        fill="white",
                        font=("Segoe UI", 12, "bold")
                    )

    def validate_grid(self):
        """Validate that the grid has all required elements for evacuation"""
        has_person = False
        has_exit = False
        has_wall = False
        has_fire = False
        
        person_count = 0
        exit_count = 0
        
        for r in range(ROWS):
            for c in range(COLS):
                cell = self.grid[r][c]
                if cell == PERSON:
                    has_person = True
                    person_count += 1
                elif cell == EXIT:
                    has_exit = True
                    exit_count += 1
                elif cell == WALL:
                    has_wall = True
                elif cell == FIRE:
                    has_fire = True
        
        errors = []
        warnings = []
        
        # Required elements
        if not has_person:
            errors.append("Person")
        elif person_count > 1:
            warnings.append(f"Multiple persons ({person_count}) - using first one")
        
        if not has_exit:
            errors.append("Exit")
        elif exit_count == 0:
            errors.append("Exit")
        
        # Optional but recommended
        if not has_wall:
            warnings.append("No walls placed")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'has_person': has_person,
            'has_exit': has_exit,
            'person_count': person_count,
            'exit_count': exit_count
        }

    def start_evacuation(self):
        # Validate grid before starting
        validation = self.validate_grid()
        
        if not validation['valid']:
            missing = ", ".join(validation['errors'])
            error_message = f"Missing Required Elements:\n\n"
            
            if "Person" in validation['errors']:
                error_message += "❌ Person: Please place a person on the grid\n"
            if "Exit" in validation['errors']:
                error_message += "❌ Exit: Please place at least one exit on the grid\n"
            
            error_message += "\nPlease add the missing elements before starting evacuation."
            
            # Show error in messagebox
            messagebox.showerror(
                "Validation Error",
                error_message,
                icon='error'
            )
            
            # Also update status label
            self.status.config(text=f"⚠️ Missing: {missing}")
            return
        
        # Show warnings if any
        if validation['warnings']:
            warnings_text = " | ".join(validation['warnings'])
            self.status.config(text=f"ℹ️ {warnings_text}")
            self.root.update()
            self.root.after(2000)  # Show warning for 2 seconds
        
        self.status.config(text="⏳ Calculating path...")
        self.root.update()
        
        # تنظيف المسارات القديمة
        for r in range(ROWS):
            for c in range(COLS):
                if self.grid[r][c] == PATH:
                    self.grid[r][c] = EMPTY

        # البحث عن الشخص والمخارج
        start = None
        exits = []
        for r in range(ROWS):
            for c in range(COLS):
                if self.grid[r][c] == PERSON:
                    if start is None:  # Use first person if multiple
                        start = (r, c)
                elif self.grid[r][c] == EXIT:
                    exits.append((r, c))

        # Double check (shouldn't happen after validation, but safety check)
        if not start:
            messagebox.showerror(
                "Error",
                "Person not found on grid!\n\nPlease place a person on the grid before starting evacuation.",
                icon='error'
            )
            self.status.config(text="❌ Error: Person not found on grid!")
            return
        
        if not exits:
            messagebox.showerror(
                "Error",
                "No exits found on grid!\n\nPlease place at least one exit on the grid before starting evacuation.",
                icon='error'
            )
            self.status.config(text="❌ Error: No exits found on grid!")
            return

        # Calculate path
        path = astar(self.grid, start, exits)

        if path is None:
            # Check if person is completely blocked
            blocked = True
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = start[0] + dx, start[1] + dy
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    if self.grid[nr][nc] not in (WALL, FIRE):
                        blocked = False
                        break
            
            if blocked:
                error_msg = "Person is Completely Blocked!\n\n"
                error_msg += "The person cannot move because all surrounding cells are blocked by walls or fire.\n\n"
                error_msg += "Please remove walls or fire around the person to create a path."
                
                messagebox.showerror(
                    "No Path Found",
                    error_msg,
                    icon='error'
                )
                self.status.config(text="❌ Person is completely blocked! Remove surrounding walls/fire.")
                self.highlight_problem_areas(start, exits)
                return
            
            # Check if exits are reachable (at least one adjacent cell is not wall/fire)
            exits_reachable = False
            for exit_pos in exits:
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nr, nc = exit_pos[0] + dx, exit_pos[1] + dy
                    if 0 <= nr < ROWS and 0 <= nc < COLS:
                        if self.grid[nr][nc] not in (WALL, FIRE):
                            exits_reachable = True
                            break
                if exits_reachable:
                    break
            
            if not exits_reachable:
                error_msg = "All Exits are Blocked!\n\n"
                error_msg += "None of the exits are accessible because all paths to them are blocked.\n\n"
                error_msg += "Please clear paths to the exits or add new accessible exits."
                
                messagebox.showerror(
                    "No Path Found",
                    error_msg,
                    icon='error'
                )
                self.status.config(text="❌ All exits are blocked! Clear paths to exits.")
                self.highlight_problem_areas(start, exits)
                return
            
            # Provide helpful suggestions for general no-path case
            suggestions = []
            if validation['exit_count'] == 1:
                suggestions.append("• Add more exits")
            if validation['has_wall']:
                suggestions.append("• Check if walls block the path")
            if validation['has_fire']:
                suggestions.append("• Fire may be blocking the route")
            suggestions.append("• Ensure a clear route exists from person to exit")
            
            error_msg = "No Safe Path Found!\n\n"
            error_msg += "The A* algorithm could not find a safe path from the person to any exit.\n\n"
            error_msg += "Suggestions:\n" + "\n".join(suggestions)
            
            messagebox.showerror(
                "No Path Found",
                error_msg,
                icon='error'
            )
            
            suggestion_text = " | ".join([s.replace("• ", "") for s in suggestions])
            self.status.config(text=f"❌ No safe path found! {suggestion_text}")
            
            # Visual feedback: highlight person and exits
            self.highlight_problem_areas(start, exits)
            return

        # Success - display path
        path_length = len(path)
        self.status.config(text=f"✅ Path found! Distance: {path_length} cells")

        for r, c in path:
            if self.grid[r][c] == EMPTY:
                self.grid[r][c] = PATH

        self.draw_grid()
    
    def highlight_problem_areas(self, start, exits):
        """Temporarily highlight person and exits when no path is found"""
        # The grid is already drawn, but we can add visual feedback
        # by ensuring person and exits are clearly visible
        # This is handled in draw_grid, but we could add a blinking effect
        pass
    def reset_grid(self):
        self.grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.draw_grid()
        self.status.config(text="🔄 Grid reset. Ready to build map")
        # Update status after a brief delay to show current state
        self.root.after(500, self.update_grid_status)
    
    def load_initial_scenario(self):
        """
        Load a predefined initial evacuation scenario
        """
        # تفريغ الشبكة أولاً
        self.grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

        # 🧍‍♂️ الشخص
        self.grid[7][2] = PERSON

        # 🚪 المخرج
        self.grid[1][13] = EXIT

        # 🔥 الحريق
        fire_positions = [
            (4, 5), (4, 6), (5, 5), (5, 6),
            (6, 6)
        ]
        for r, c in fire_positions:
            self.grid[r][c] = FIRE

        # 🧱 الجدران (لجعل السيناريو واقعي)
        wall_positions = [
            (2, 3), (2, 4), (2, 5),
            (3, 3),
            (6, 3), (7, 3), (8, 3),
            (8, 4), (8, 5)
        ]
        for r, c in wall_positions:
            self.grid[r][c] = WALL

        # تحديث الواجهة والحالة
        self.draw_grid()
        self.status.config(
            text="📍 Initial scenario loaded: Person, Fire, Exit"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = EvacuationGUI(root)
    root.mainloop()
