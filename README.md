# Habit Tracker  

#### Video Demo: [Watch Here](https://youtu.be/-h-Wo5ASOhE)  

## **Description**  
Habit Tracker is a **Python-based application** designed to help users build, maintain, and track daily habits efficiently. This project includes both a **CLI** and a **GUI** using Tkinter.  

Users can:  
- **Add new habits** to track.  
- **Log habit completions** to maintain consistency.  
- **Monitor streaks** to stay motivated.  
- **View and manage habits** through an intuitive GUI.  

Habit data is stored in a **JSON file**, ensuring persistence between sessions, and the application includes **automated tests using `pytest`** to maintain reliability.  

---

## **Features**  
✅ **Command-Line & GUI Interface** – Choose between text-based and graphical interactions.  
✅ **Add & Track Habits** – Easily log completions and view habit streaks.  
✅ **Streak Calculation** – Automatically calculates the current streak for each habit.  
✅ **Persistent Data Storage** – Saves habit progress in a JSON file.  
✅ **Automated Testing** – Uses `pytest` for reliability.  

---

## **Project Structure**  

This project consists of the following main files:  

### **1️⃣ `project.py` (CLI Mode)**  
Handles the main habit tracking functionality:  
- **Loading & saving habit data**  
- **Adding habits**  
- **Logging habit completions**  
- **Checking streaks**  

### **2️⃣ `habit_tracker_gui.py` (GUI Mode)**  
Provides a **Tkinter-based GUI** for a more user-friendly experience:  
- Displays a list of habits with **streak counts & last logged date**.  
- Allows **adding new habits** through an input box.  
- Enables **logging habit completions** with a button click.  
- Uses a **treeview widget** to display habits in a structured way. 

### **3️⃣ `test_project.py` (Unit Tests)**  
This file contains automated tests using `pytest` to ensure the correctness of the habit tracker. It tests:  
- Habit data loading and saving.  
- Adding new habits.  
- Logging habit completions. 