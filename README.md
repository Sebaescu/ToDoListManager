# To-Do List Manager

A command-line application for managing tasks with support for adding, listing, completing, and clearing tasks.

## Features

- **Add tasks** with title, description, priority, and due date
- **List tasks** with filtering by status (pending/completed)
- **Mark tasks as completed** by ID or title
- **Clear all tasks** from the list
- **View statistics** about your tasks
- **Persistent storage** using JSON files
- **Colored output** for better readability
- **BDD testing** with Behave
- **Unit testing** with pytest

## Task Attributes

Each task has the following attributes:
- **ID**: Unique identifier (auto-generated)
- **Title**: Task name (required)
- **Description**: Detailed description (optional)
- **Priority**: low, medium, or high (default: medium)
- **Due Date**: Optional due date
- **Status**: pending or completed
- **Created At**: Timestamp when task was created
- **Completed At**: Timestamp when task was completed (if applicable)

## Requirements

- Python 3.x
- Required packages (install via `pip install -r requirements.txt`):
  - behave==1.2.6
  - pytest==7.4.4
  - colorama==0.4.6

## Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

#### Add a task
```bash
python cli.py add "Buy groceries"
python cli.py add "Buy groceries" --description "Get milk, bread, and eggs" --priority high --due-date 2024-12-31
```

#### List tasks
```bash
python cli.py list                    # List all tasks
python cli.py list --status pending   # List only pending tasks
python cli.py list --status completed # List only completed tasks
```

#### Mark task as completed
```bash
python cli.py complete "Buy groceries"  # By title
python cli.py complete 1                # By ID
```

#### Clear all tasks
```bash
python cli.py clear
```

#### View statistics
```bash
python cli.py stats
```

#### Help
```bash
python cli.py --help
python cli.py add --help
```

### Python API

You can also use the ToDoListManager class directly in your Python code:

```python
from todo_list import ToDoListManager

# Create a manager
todo = ToDoListManager()

# Add tasks
task1 = todo.add_task("Buy groceries", "Get milk and bread", "high")
task2 = todo.add_task("Pay bills")

# List tasks
all_tasks = todo.list_tasks()
pending_tasks = todo.list_tasks("pending")

# Mark as completed
todo.mark_task_completed("Buy groceries")  # By title
todo.mark_task_completed(1)                # By ID

# Clear all
todo.clear_all_tasks()
```

## Testing

### Run Unit Tests (pytest)
```bash
pytest tests/ -v
```

### Run BDD Tests (Behave)
```bash
behave features/
```

### Run All Tests
```bash
pytest tests/ -v && behave features/
```

## Project Structure

```
ToDoList/
├── todo_list.py              # Main application logic
├── cli.py                    # Command-line interface
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── features/                # Behave feature files
│   ├── todo_list.feature    # BDD scenarios
│   └── steps/
│       └── todo_list_steps.py # Step definitions
└── tests/                   # pytest test files
    ├── test_todo_list.py    # Unit tests for core logic
    └── test_cli.py          # Unit tests for CLI
```

## Example Output

```
$ python cli.py add "Buy groceries" --priority high
✓ Added task: Buy groceries

$ python cli.py add "Pay bills" --description "Electricity and water"
✓ Added task: Pay bills

$ python cli.py list

Tasks:
  ○ [1] Buy groceries ●●●
  ○ [2] Pay bills ●●
    Description: Electricity and water

$ python cli.py complete 1
✓ Marked task as completed: 1

$ python cli.py stats

Task Statistics:
  Total tasks: 2
  Pending: 1
  Completed: 1
  Completion rate: 50.0%
```

## BDD Scenarios

The application includes comprehensive BDD tests covering:

- Adding tasks to the to-do list
- Listing all tasks
- Marking tasks as completed (by title and ID)
- Clearing the entire to-do list
- Filtering tasks by status
- Error handling for non-existent tasks

Run BDD tests with: `behave features/`

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is open source and available under the MIT License.
