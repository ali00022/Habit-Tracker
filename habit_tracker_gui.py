import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from project import add_habit, log_habit, get_streak, load_habits

class HabitTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Habit Tracker")
        self.root.geometry("480x400")
        self.root.configure(bg="#f5f5f5")
        
        # Set theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#f5f5f5')
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TLabel', background='#f5f5f5', font=('Arial', 11))
        self.style.configure('Header.TLabel', font=('Arial', 16, 'bold'))
        
        self.setup_ui()
        self.update_habit_list()
    
    def setup_ui(self):
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=10, padx=20, fill='x')
        
        header_label = ttk.Label(
            header_frame, 
            text="Daily Habit Tracker", 
            style='Header.TLabel'
        )
        header_label.pack()
        
        # Add Habit Section
        add_frame = ttk.Frame(self.root)
        add_frame.pack(pady=10, padx=20, fill='x')
        
        ttk.Label(add_frame, text="New Habit:").grid(row=0, column=0, padx=5, pady=5)
        self.habit_entry = ttk.Entry(add_frame, width=30)
        self.habit_entry.grid(row=0, column=1, padx=5, pady=5)
        
        add_button = ttk.Button(
            add_frame, 
            text="Add Habit",
            command=self.handle_add_habit
        )
        add_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Habit List Section
        list_frame = ttk.Frame(self.root)
        list_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        ttk.Label(list_frame, text="Your Habits:").pack(anchor='w')
        
        # Create Treeview (coloums in the gui)
        columns = ('habit', 'streak', 'last_logged')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=8)
        
        # Define headings
        self.tree.heading('habit', text='Habit')
        self.tree.heading('streak', text='Current Streak')
        self.tree.heading('last_logged', text='Last Logged')
        
        # Column widths
        self.tree.column('habit', width=200)
        self.tree.column('streak', width=100)
        self.tree.column('last_logged', width=120)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Action buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10, padx=20, fill='x')
        
        log_button = ttk.Button(
            button_frame,
            text="Log Completion",
            command=self.handle_log_habit
        )
        log_button.pack(side='left', padx=5)
        
        refresh_button = ttk.Button(
            button_frame,
            text="Refresh List",
            command=self.update_habit_list
        )
        refresh_button.pack(side='right', padx=5)
        
        # Status message
        self.status_var = tk.StringVar()
        status_label = ttk.Label(
            self.root, 
            textvariable=self.status_var,
            font=('Arial', 10, 'italic')
        )
        status_label.pack(pady=5)
    
    def handle_add_habit(self):
        habit_name = self.habit_entry.get().strip()
        if not habit_name:
            self.status_var.set("Please enter a habit name")
            return
            
        result = add_habit(habit_name)
        self.status_var.set(result)
        self.habit_entry.delete(0, 'end')
        self.update_habit_list()
    
    def handle_log_habit(self):
        selected = self.tree.selection()
        if not selected:
            self.status_var.set("Please select a habit to log")
            return
            
        habit_name = self.tree.item(selected[0])['values'][0]
        result = log_habit(habit_name)
        self.status_var.set(result)
        self.update_habit_list()
    
    def update_habit_list(self):
        """Refresh the habit list display"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Load habits from jason file and update the gui using Treeview
        habits = load_habits()
        for habit_name, dates in habits.items():
            streak = get_streak(habit_name)
            
            # Get last logged date
            last_logged = "Never"
            if dates:
                sorted_dates = sorted(dates, reverse=True)
                last_date = datetime.date.fromisoformat(sorted_dates[0])
                last_logged = last_date.strftime("%b %d, %Y")
            
            self.tree.insert('', 'end', values=(habit_name, streak, last_logged))

if __name__ == "__main__":
    root = tk.Tk()
    app = HabitTrackerApp(root)
    root.mainloop()
