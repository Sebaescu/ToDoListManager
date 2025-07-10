Feature: To-Do List Manager
  As a user
  I want to manage my tasks
  So that I can stay organized and productive

  Scenario: Add a task to the to-do list
    Given the to-do list is empty
    When the user adds a task "Buy groceries"
    Then the to-do list should contain "Buy groceries"

  Scenario: Add a task with description and priority
    Given the to-do list is empty
    When the user adds a task "Buy groceries" with description "Get milk, bread, and eggs" and priority "high"
    Then the to-do list should contain "Buy groceries"
    And the task should have description "Get milk, bread, and eggs"
    And the task should have priority "high"

  Scenario: List all tasks in the to-do list
    Given the to-do list contains tasks:
      | Task        |
      | Buy groceries |
      | Pay bills     |
    When the user lists all tasks
    Then the output should contain:
      """
      Tasks:
        ○ [1] Buy groceries ●●
        ○ [2] Pay bills ●●
      """

  Scenario: Mark a task as completed by title
    Given the to-do list contains tasks:
      | Task        | Status  |
      | Buy groceries | pending |
    When the user marks task "Buy groceries" as completed
    Then the to-do list should show task "Buy groceries" as completed

  Scenario: Mark a task as completed by ID
    Given the to-do list contains tasks:
      | Task        | Status  |
      | Buy groceries | pending |
    When the user marks task with ID 1 as completed
    Then the to-do list should show task "Buy groceries" as completed

  Scenario: Clear the entire to-do list
    Given the to-do list contains tasks:
      | Task        |
      | Buy groceries |
      | Pay bills     |
    When the user clears the to-do list
    Then the to-do list should be empty

  Scenario: List only pending tasks
    Given the to-do list contains tasks:
      | Task        | Status    |
      | Buy groceries | pending   |
      | Pay bills     | completed |
    When the user lists pending tasks
    Then the output should contain only pending tasks

  Scenario: List only completed tasks
    Given the to-do list contains tasks:
      | Task        | Status    |
      | Buy groceries | pending   |
      | Pay bills     | completed |
    When the user lists completed tasks
    Then the output should contain only completed tasks

  Scenario: Try to mark non-existent task as completed
    Given the to-do list is empty
    When the user tries to mark task "Non-existent task" as completed
    Then the operation should fail
    And the to-do list should remain empty
