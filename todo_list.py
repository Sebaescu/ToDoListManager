from datetime import datetime
from typing import List, Dict, Optional
import json
import os


class Task:
    """Represents a single task in the to-do list."""
    
    def __init__(self, title: str, description: str = "", priority: str = "medium", due_date: Optional[str] = None):
        self.id = None  # Will be assigned when added to the list
        self.title = title
        self.description = description
        self.priority = priority  # low, medium, high
        self.due_date = due_date
        self.status = "pending"  # pending, completed
        self.created_at = datetime.now().isoformat()
        self.completed_at = None
    
    def mark_completed(self):
        """Mark the task as completed."""
        self.status = "completed"
        self.completed_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'due_date': self.due_date,
            'status': self.status,
            'created_at': self.created_at,
            'completed_at': self.completed_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """Create task from dictionary."""
        task = cls(
            title=data['title'],
            description=data.get('description', ''),
            priority=data.get('priority', 'medium'),
            due_date=data.get('due_date')
        )
        task.id = data.get('id')
        task.status = data.get('status', 'pending')
        task.created_at = data.get('created_at', datetime.now().isoformat())
        task.completed_at = data.get('completed_at')
        return task
    
    def __str__(self) -> str:
        status_symbol = "✓" if self.status == "completed" else "○"
        priority_symbol = {"low": "●", "medium": "●●", "high": "●●●"}[self.priority]
        return f"{status_symbol} [{self.id}] {self.title} {priority_symbol}"


class ToDoListManager:
    """Main class for managing the to-do list."""
    
    def __init__(self, data_file: str = "todo_list.json"):
        self.data_file = data_file
        self.tasks: List[Task] = []
        self.next_id = 1
        self.load_tasks()
    
    def add_task(self, title: str, description: str = "", priority: str = "medium", due_date: Optional[str] = None) -> Task:
        """Add a new task to the to-do list."""
        task = Task(title, description, priority, due_date)
        task.id = self.next_id
        self.next_id += 1
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def list_tasks(self, status_filter: Optional[str] = None) -> List[Task]:
        """List all tasks, optionally filtered by status."""
        if status_filter:
            return [task for task in self.tasks if task.status == status_filter]
        return self.tasks.copy()
    
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get a task by its ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_task_by_title(self, title: str) -> Optional[Task]:
        """Get a task by its title."""
        for task in self.tasks:
            if task.title.lower() == title.lower():
                return task
        return None
    
    def mark_task_completed(self, identifier) -> bool:
        """Mark a task as completed by ID or title."""
        task = None
        if isinstance(identifier, int):
            task = self.get_task_by_id(identifier)
        elif isinstance(identifier, str):
            # Try to convert to int first (ID), then search by title
            try:
                task_id = int(identifier)
                task = self.get_task_by_id(task_id)
            except ValueError:
                task = self.get_task_by_title(identifier)
        
        if task:
            task.mark_completed()
            self.save_tasks()
            return True
        return False
    
    def clear_all_tasks(self):
        """Clear all tasks from the to-do list."""
        self.tasks.clear()
        self.next_id = 1
        self.save_tasks()
    
    def save_tasks(self):
        """Save tasks to JSON file."""
        data = {
            'next_id': self.next_id,
            'tasks': [task.to_dict() for task in self.tasks]
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_tasks(self):
        """Load tasks from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                self.next_id = data.get('next_id', 1)
                self.tasks = [Task.from_dict(task_data) for task_data in data.get('tasks', [])]
            except (json.JSONDecodeError, KeyError):
                # If file is corrupted, start fresh
                self.tasks = []
                self.next_id = 1
    
    def is_empty(self) -> bool:
        """Check if the to-do list is empty."""
        return len(self.tasks) == 0
    
    def count_tasks(self, status: Optional[str] = None) -> int:
        """Count tasks, optionally filtered by status."""
        if status:
            return len([task for task in self.tasks if task.status == status])
        return len(self.tasks)
