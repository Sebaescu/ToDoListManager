#!/usr/bin/env python3
"""
To-Do List Manager CLI Application
A command-line interface for managing tasks.
"""

import argparse
import sys
from todo_list import ToDoListManager
from colorama import init, Fore, Style

# Initialize colorama for Windows compatibility
init()


def print_colored(text: str, color: str = Fore.WHITE):
    """Print colored text."""
    print(f"{color}{text}{Style.RESET_ALL}")


def print_tasks(tasks, title="Tasks"):
    """Print a list of tasks in a formatted way."""
    if not tasks:
        print_colored("No tasks found.", Fore.YELLOW)
        return
    
    print_colored(f"\n{title}:", Fore.CYAN)
    for task in tasks:
        color = Fore.GREEN if task.status == "completed" else Fore.WHITE
        print_colored(f"  {task}", color)
        if task.description:
            print_colored(f"    Description: {task.description}", Fore.LIGHTBLACK_EX)
        if task.due_date:
            print_colored(f"    Due: {task.due_date}", Fore.LIGHTBLACK_EX)


def main():
    parser = argparse.ArgumentParser(description="To-Do List Manager")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add task command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('title', help='Task title')
    add_parser.add_argument('--description', '-d', default='', help='Task description')
    add_parser.add_argument('--priority', '-p', choices=['low', 'medium', 'high'], 
                           default='medium', help='Task priority')
    add_parser.add_argument('--due-date', help='Due date (YYYY-MM-DD format)')
    
    # List tasks command
    list_parser = subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument('--status', choices=['pending', 'completed'], 
                            help='Filter by status')
    
    # Complete task command
    complete_parser = subparsers.add_parser('complete', help='Mark a task as completed')
    complete_parser.add_argument('identifier', help='Task ID or title')
    
    # Clear command
    subparsers.add_parser('clear', help='Clear all tasks')
    
    # Stats command
    subparsers.add_parser('stats', help='Show task statistics')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize the to-do list manager
    todo_manager = ToDoListManager()
    
    try:
        if args.command == 'add':
            task = todo_manager.add_task(
                title=args.title,
                description=args.description,
                priority=args.priority,
                due_date=args.due_date
            )
            print_colored(f"✓ Added task: {task.title}", Fore.GREEN)
        
        elif args.command == 'list':
            tasks = todo_manager.list_tasks(args.status)
            status_text = f" ({args.status})" if args.status else ""
            print_tasks(tasks, f"Tasks{status_text}")
        
        elif args.command == 'complete':
            if todo_manager.mark_task_completed(args.identifier):
                print_colored(f"✓ Marked task as completed: {args.identifier}", Fore.GREEN)
            else:
                print_colored(f"✗ Task not found: {args.identifier}", Fore.RED)
        
        elif args.command == 'clear':
            if todo_manager.is_empty():
                print_colored("To-do list is already empty.", Fore.YELLOW)
            else:
                todo_manager.clear_all_tasks()
                print_colored("✓ Cleared all tasks from the to-do list.", Fore.GREEN)
        
        elif args.command == 'stats':
            total = todo_manager.count_tasks()
            pending = todo_manager.count_tasks('pending')
            completed = todo_manager.count_tasks('completed')
            
            print_colored("\nTask Statistics:", Fore.CYAN)
            print_colored(f"  Total tasks: {total}", Fore.WHITE)
            print_colored(f"  Pending: {pending}", Fore.YELLOW)
            print_colored(f"  Completed: {completed}", Fore.GREEN)
            
            if total > 0:
                completion_rate = (completed / total) * 100
                print_colored(f"  Completion rate: {completion_rate:.1f}%", Fore.BLUE)
    
    except Exception as e:
        print_colored(f"Error: {str(e)}", Fore.RED)
        sys.exit(1)


if __name__ == "__main__":
    main()
