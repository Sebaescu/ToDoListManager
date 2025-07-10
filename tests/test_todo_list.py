import pytest
import tempfile
import os
from todo_list import ToDoListManager, Task


@pytest.fixture
def temp_todo_manager():
    """Create a temporary ToDoListManager for testing."""
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
    temp_file.close()
    
    manager = ToDoListManager(temp_file.name)
    manager.clear_all_tasks()
    
    yield manager
    
    # Cleanup
    try:
        os.unlink(temp_file.name)
    except FileNotFoundError:
        pass


@pytest.fixture
def sample_tasks():
    """Create sample tasks for testing."""
    return [
        {"title": "Buy groceries", "description": "Get milk, bread, and eggs", "priority": "high"},
        {"title": "Pay bills", "description": "Electricity and water bills", "priority": "medium"},
        {"title": "Call dentist", "description": "", "priority": "low"},
    ]


class TestTask:
    """Test the Task class."""
    
    def test_task_creation(self):
        """Test creating a new task."""
        task = Task("Buy groceries", "Get milk and bread", "high", "2024-12-31")
        
        assert task.title == "Buy groceries"
        assert task.description == "Get milk and bread"
        assert task.priority == "high"
        assert task.due_date == "2024-12-31"
        assert task.status == "pending"
        assert task.id is None
        assert task.created_at is not None
        assert task.completed_at is None
    
    def test_task_mark_completed(self):
        """Test marking a task as completed."""
        task = Task("Test task")
        assert task.status == "pending"
        assert task.completed_at is None
        
        task.mark_completed()
        
        assert task.status == "completed"
        assert task.completed_at is not None
    
    def test_task_to_dict(self):
        """Test converting task to dictionary."""
        task = Task("Test task", "Test description", "high", "2024-12-31")
        task.id = 1
        
        task_dict = task.to_dict()
        
        assert task_dict['id'] == 1
        assert task_dict['title'] == "Test task"
        assert task_dict['description'] == "Test description"
        assert task_dict['priority'] == "high"
        assert task_dict['due_date'] == "2024-12-31"
        assert task_dict['status'] == "pending"
    
    def test_task_from_dict(self):
        """Test creating task from dictionary."""
        task_data = {
            'id': 1,
            'title': "Test task",
            'description': "Test description",
            'priority': "high",
            'due_date': "2024-12-31",
            'status': "completed"
        }
        
        task = Task.from_dict(task_data)
        
        assert task.id == 1
        assert task.title == "Test task"
        assert task.description == "Test description"
        assert task.priority == "high"
        assert task.due_date == "2024-12-31"
        assert task.status == "completed"
    
    def test_task_string_representation(self):
        """Test string representation of task."""
        task = Task("Test task")
        task.id = 1
        
        str_repr = str(task)
        
        assert "○" in str_repr  # Pending symbol
        assert "[1]" in str_repr  # ID
        assert "Test task" in str_repr  # Title
        assert "●●" in str_repr  # Medium priority
        
        task.mark_completed()
        str_repr = str(task)
        
        assert "✓" in str_repr  # Completed symbol


class TestToDoListManager:
    """Test the ToDoListManager class."""
    
    def test_empty_todo_list(self, temp_todo_manager):
        """Test empty to-do list."""
        assert temp_todo_manager.is_empty()
        assert temp_todo_manager.count_tasks() == 0
        assert len(temp_todo_manager.list_tasks()) == 0
    
    def test_add_task(self, temp_todo_manager):
        """Test adding a task."""
        task = temp_todo_manager.add_task("Buy groceries", "Get milk and bread", "high")
        
        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == "Get milk and bread"
        assert task.priority == "high"
        assert not temp_todo_manager.is_empty()
        assert temp_todo_manager.count_tasks() == 1
    
    def test_add_multiple_tasks(self, temp_todo_manager, sample_tasks):
        """Test adding multiple tasks."""
        added_tasks = []
        for task_data in sample_tasks:
            task = temp_todo_manager.add_task(**task_data)
            added_tasks.append(task)
        
        assert temp_todo_manager.count_tasks() == 3
        assert not temp_todo_manager.is_empty()
        
        # Check IDs are sequential
        for i, task in enumerate(added_tasks, 1):
            assert task.id == i
    
    def test_list_tasks(self, temp_todo_manager, sample_tasks):
        """Test listing tasks."""
        # Add sample tasks
        for task_data in sample_tasks:
            temp_todo_manager.add_task(**task_data)
        
        all_tasks = temp_todo_manager.list_tasks()
        assert len(all_tasks) == 3
        
        # Test titles
        titles = [task.title for task in all_tasks]
        assert "Buy groceries" in titles
        assert "Pay bills" in titles
        assert "Call dentist" in titles
    
    def test_get_task_by_id(self, temp_todo_manager):
        """Test getting task by ID."""
        task = temp_todo_manager.add_task("Test task")
        
        found_task = temp_todo_manager.get_task_by_id(1)
        assert found_task is not None
        assert found_task.id == 1
        assert found_task.title == "Test task"
        
        not_found = temp_todo_manager.get_task_by_id(999)
        assert not_found is None
    
    def test_get_task_by_title(self, temp_todo_manager):
        """Test getting task by title."""
        temp_todo_manager.add_task("Buy groceries")
        
        found_task = temp_todo_manager.get_task_by_title("Buy groceries")
        assert found_task is not None
        assert found_task.title == "Buy groceries"
        
        # Test case-insensitive search
        found_task_lower = temp_todo_manager.get_task_by_title("buy groceries")
        assert found_task_lower is not None
        
        not_found = temp_todo_manager.get_task_by_title("Nonexistent task")
        assert not_found is None
    
    def test_mark_task_completed_by_id(self, temp_todo_manager):
        """Test marking task as completed by ID."""
        task = temp_todo_manager.add_task("Test task")
        assert task.status == "pending"
        
        result = temp_todo_manager.mark_task_completed(1)
        assert result is True
        
        found_task = temp_todo_manager.get_task_by_id(1)
        assert found_task.status == "completed"
        assert found_task.completed_at is not None
    
    def test_mark_task_completed_by_title(self, temp_todo_manager):
        """Test marking task as completed by title."""
        temp_todo_manager.add_task("Buy groceries")
        
        result = temp_todo_manager.mark_task_completed("Buy groceries")
        assert result is True
        
        found_task = temp_todo_manager.get_task_by_title("Buy groceries")
        assert found_task.status == "completed"
    
    def test_mark_task_completed_by_string_id(self, temp_todo_manager):
        """Test marking task as completed by string ID."""
        temp_todo_manager.add_task("Test task")
        
        result = temp_todo_manager.mark_task_completed("1")
        assert result is True
        
        found_task = temp_todo_manager.get_task_by_id(1)
        assert found_task.status == "completed"
    
    def test_mark_nonexistent_task_completed(self, temp_todo_manager):
        """Test marking non-existent task as completed."""
        result = temp_todo_manager.mark_task_completed("Nonexistent task")
        assert result is False
        
        result = temp_todo_manager.mark_task_completed(999)
        assert result is False
    
    def test_list_tasks_by_status(self, temp_todo_manager):
        """Test listing tasks filtered by status."""
        # Add tasks
        task1 = temp_todo_manager.add_task("Task 1")
        task2 = temp_todo_manager.add_task("Task 2")
        task3 = temp_todo_manager.add_task("Task 3")
        
        # Mark some as completed
        task1.mark_completed()
        task3.mark_completed()
        temp_todo_manager.save_tasks()
        
        # Test filtering
        pending_tasks = temp_todo_manager.list_tasks("pending")
        assert len(pending_tasks) == 1
        assert pending_tasks[0].title == "Task 2"
        
        completed_tasks = temp_todo_manager.list_tasks("completed")
        assert len(completed_tasks) == 2
        completed_titles = [task.title for task in completed_tasks]
        assert "Task 1" in completed_titles
        assert "Task 3" in completed_titles
    
    def test_count_tasks(self, temp_todo_manager):
        """Test counting tasks."""
        assert temp_todo_manager.count_tasks() == 0
        assert temp_todo_manager.count_tasks("pending") == 0
        assert temp_todo_manager.count_tasks("completed") == 0
        
        # Add tasks
        task1 = temp_todo_manager.add_task("Task 1")
        task2 = temp_todo_manager.add_task("Task 2")
        
        assert temp_todo_manager.count_tasks() == 2
        assert temp_todo_manager.count_tasks("pending") == 2
        assert temp_todo_manager.count_tasks("completed") == 0
        
        # Complete one task
        task1.mark_completed()
        temp_todo_manager.save_tasks()
        
        assert temp_todo_manager.count_tasks() == 2
        assert temp_todo_manager.count_tasks("pending") == 1
        assert temp_todo_manager.count_tasks("completed") == 1
    
    def test_clear_all_tasks(self, temp_todo_manager, sample_tasks):
        """Test clearing all tasks."""
        # Add sample tasks
        for task_data in sample_tasks:
            temp_todo_manager.add_task(**task_data)
        
        assert temp_todo_manager.count_tasks() == 3
        assert not temp_todo_manager.is_empty()
        
        temp_todo_manager.clear_all_tasks()
        
        assert temp_todo_manager.count_tasks() == 0
        assert temp_todo_manager.is_empty()
        assert temp_todo_manager.next_id == 1
    
    def test_save_and_load_tasks(self, temp_todo_manager):
        """Test saving and loading tasks from file."""
        # Add a task
        original_task = temp_todo_manager.add_task("Test task", "Test description", "high")
        original_task.mark_completed()
        temp_todo_manager.save_tasks()
        
        # Create a new manager with the same file
        new_manager = ToDoListManager(temp_todo_manager.data_file)
        
        assert new_manager.count_tasks() == 1
        assert new_manager.next_id == 2
        
        loaded_task = new_manager.get_task_by_id(1)
        assert loaded_task is not None
        assert loaded_task.title == "Test task"
        assert loaded_task.description == "Test description"
        assert loaded_task.priority == "high"
        assert loaded_task.status == "completed"
