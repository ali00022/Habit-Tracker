import os
import json
import datetime
import logging

# Logging Setup
logging.basicConfig(filename="habit_tracker.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Folder & File Setup
DATA_FOLDER = "Project"
FILE_PATH = os.path.join(DATA_FOLDER, "habit_data.json")

# Ensure directory exists
os.makedirs(DATA_FOLDER, exist_ok=True)

# Cache habit data to avoid frequent file reads
habit_cache = {}

def main():
    """
    Main function to demonstrate the habit tracker functionality.
    For a full GUI interface, use the tkinter implementation separately.
    """
    # Display welcome message
    print("\n🌟 Welcome to Habit Tracker 🌟")
    print("=" * 40)
    
    # Demonstrate adding habits
    print("\n📝 Adding Habits:")
    print(add_habit("Morning Run"))
    print(add_habit("Read a Book"))
    print(add_habit("Meditation"))
    
    # Demonstrate logging habits
    print("\n✅ Logging Habits:")
    print(log_habit("Morning Run"))
    print(log_habit("Read a Book"))
    
    # Try logging the same habit twice
    print("\n⚠️ Testing duplicate logging:")
    print(log_habit("Morning Run"))
    
    # Check streaks
    print("\n🔥 Current Streaks:")
    print(f"Morning Run: {get_streak('Morning Run')}")
    print(f"Read a Book: {get_streak('Read a Book')}")
    print(f"Meditation: {get_streak('Meditation')}")
    
    print("\n💡 To use the full GUI version, run the habit_tracker_gui.py file")

def save_habits(habits=None):
    """
    Save habits data to JSON file.
    
    """
    global habit_cache
    if habits is None:
        habits = {}
    habit_cache = habits  # Update cache
    try:
        with open(FILE_PATH, "w") as f:
            json.dump(habits, f, indent=4)
    except IOError as e:
        logging.error(f"Failed to save habits: {e}")

def load_habits():
    """
    Load habits from JSON file with caching for efficiency and returning a dictionary of habits.
    """
    global habit_cache
    if habit_cache:
        return habit_cache  # Use cache if available

    if not os.path.exists(FILE_PATH):
        habit_cache = {}
        return habit_cache

    try:
        with open(FILE_PATH, "r") as f:
            habit_cache = json.load(f) or {}
            return habit_cache
    except json.JSONDecodeError:
        logging.warning("Corrupt JSON detected.")
        habit_cache = {}
        save_habits(habit_cache)  # Reset corrupted file
    return habit_cache

def add_habit(new_habit):
    """
    Add a new habit to track.
    """
    habits = load_habits()
    new_habit = new_habit.strip()

    if not new_habit:
        return "Please enter a habit!"

    if new_habit in habits:
        return "That habit already exists!"

    habits[new_habit] = []
    save_habits(habits)
    logging.info(f"Habit added: {new_habit}")

    return f"Added: {new_habit}"

def log_habit(habit_name):
    """
    Log completion of a habit for today.
    """
    habits = load_habits()
    today = datetime.date.today().isoformat()

    if habit_name not in habits:
        return "Select a habit first!"

    if today in habits[habit_name]:
        return "Already logged today!"

    habits[habit_name].append(today)
    save_habits(habits)
    logging.info(f"Logged: {habit_name} on {today}")

    return f"Logged {habit_name} today!"

def get_streak(habit_name):
    """
    Calculate the current streak for a habit and return a the number of days the habit has been logged/ completed consecutively.
    """
    habits = load_habits()

    if habit_name not in habits:
        return "Pick a habit first!"

    dates = sorted(set(habits[habit_name]), reverse=True)
    today = datetime.date.today()

    if not dates or dates[0] != today.isoformat():
        return "No streak today."

    # Efficient streak counting
    streak = 1
    for prev, curr in zip(dates, dates[1:]):
        if (datetime.date.fromisoformat(prev) - datetime.date.fromisoformat(curr)).days == 1:
            streak += 1
        else:
            break

    return f"🔥 Streak: {streak} days"

if __name__ == "__main__":
    main()
