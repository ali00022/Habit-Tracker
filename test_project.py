import os
import json
import datetime
import pytest
from project import add_habit, log_habit, get_streak, save_habits, load_habits

# Define test data paths - using a separate test folder
TEST_DATA_FOLDER = "Habit_Tracker"
TEST_FILE_PATH = os.path.join(TEST_DATA_FOLDER, "test_habit_data.json")

@pytest.fixture
def setup_test_env(monkeypatch):
    """
    Using monkeypatch to avoid modifying the real data file and runing the test with fake values
    """
    # Create test directory
    os.makedirs(TEST_DATA_FOLDER, exist_ok=True)
    
    # Override the FILE_PATH in the project module using monkeypatch
    import project
    monkeypatch.setattr(project, "FILE_PATH", TEST_FILE_PATH)
    
    # Clear the habit cache
    monkeypatch.setattr(project, "habit_cache", {})
    
    # Prepare test data
    test_habits = {
        "Morning Run": ["2025-01-01", "2025-01-02"],
        "Read a Book": [],
        "Meditation": []
    }
    
    # Save test data to file
    with open(TEST_FILE_PATH, "w") as f:
        json.dump(test_habits, f, indent=4)
    
    yield  # Allow tests to run
    
    # Cleanup test files after tests
    if os.path.exists(TEST_FILE_PATH):
        os.remove(TEST_FILE_PATH)
    if os.path.exists(TEST_DATA_FOLDER):
        os.rmdir(TEST_DATA_FOLDER)

def test_add_habit(setup_test_env):
    """Test adding a new habit"""
    # Add a new habit
    result = add_habit("Exercise")
    habits = load_habits()
    
    # Verify the habit was added
    assert "Exercise" in habits
    assert habits["Exercise"] == []
    assert result == "Added: Exercise"
    
    # Test adding an empty habit
    result = add_habit("  ")
    assert result == "Please enter a habit!"
    
    # Test adding a duplicate habit
    result = add_habit("Exercise")
    assert result == "That habit already exists!"

def test_log_habit(setup_test_env):
    """Test logging a habit completion"""
    # Get today's date
    today = datetime.date.today().isoformat()
    
    # Log a habit
    result = log_habit("Morning Run")
    habits = load_habits()
    
    # Verify the habit was logged
    assert today in habits["Morning Run"]
    assert result == f"Logged Morning Run today!"
    
    # Test logging again (should fail)
    result = log_habit("Morning Run")
    assert result == "Already logged today!"
    
    # Test logging non-existent habit
    result = log_habit("Non-existent Habit")
    assert result == "Select a habit first!"



# Optional extra test for load/save functionality
def test_save_load_habits(setup_test_env):
    """Test saving and loading habits"""
    # Create new habit data
    test_data = {
        "Test Habit 1": ["2025-01-01"],
        "Test Habit 2": ["2025-01-01", "2025-01-02"]
    }
    
    # Save the data
    save_habits(test_data)
    
    # Load the data and verify it matches
    loaded_data = load_habits()
    assert loaded_data == test_data
