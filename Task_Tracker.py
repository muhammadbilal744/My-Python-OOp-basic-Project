# Import dataclass and field for automatic constructor and default values
from dataclasses import dataclass, field

# Import type hints
from typing import Dict, List, Tuple, Optional

# Allowed task statuses (constant tuple)
STATUS = ("TODO", "DOING", "DONE")


# Base class for sorting strategy (Strategy Pattern)
class SortStrategy:
    # Default sort (no change)
    def sort(self, tasks: list["Task"]) -> list["Task"]:
        return tasks


# Sort tasks by priority (highest first)
class SortByPriority(SortStrategy):
    def sort(self, tasks: list["Task"]) -> list["Task"]:
        return sorted(tasks, key=lambda t: t.priority, reverse=True)


# Sort tasks by creation order (task_id)
class SortByCreated(SortStrategy):
    def sort(self, tasks: list["Task"]) -> list["Task"]:
        return sorted(tasks, key=lambda t: t.task_id)


# Task class using dataclass
@dataclass
class Task:
    task_id: int          # Unique task ID
    title: str            # Task title
    desc: str             # Task description
    priority: int         # Priority (1-5)

    # Private status variable (default TODO)
    __status: str = field(default="TODO", repr=False)

    # Set of tags (no duplicate tags allowed)
    tags: set[str] = field(default_factory=set)

    # History of status changes
    # (step_number, action_type, old_status, new_status)
    history: List[Tuple[int, str, str, str]] = field(default_factory=list)

    # Internal step counter for history tracking
    _step: int = field(default=0, repr=False)

    # Getter for status (read-only property)
    @property
    def status(self) -> str:
        return self.__status

    # Add a tag to the task
    def add_tag(self, tag: str) -> None:
        tag = tag.strip()
        if not tag:
            raise ValueError("Tag cannot be empty.")
        self.tags.add(tag)

    # Change task status
    def change_status(self, new_status: str) -> None:
        new_status = new_status.strip().upper()

        # Validate status
        if new_status not in STATUS:
            raise ValueError(f"Status must be one of {STATUS}.")

        old = self.__status  # Store old status
        self._step += 1      # Increase step number

        # Save history record
        self.history.append((self._step, "STATUS_CHANGE", old, new_status))

        # Update status
        self.__status = new_status

    # Short summary of task
    def summary(self) -> str:
        tags = ", ".join(sorted(self.tags)) if self.tags else "_"
        return f"[{self.task_id}] {self.title} | {self.status} | p={self.priority} | tags={tags}"


# Project class
class Project:
    def __init__(self, project_id: str, name: str):
        self.project_id = project_id  # Project ID
        self.name = name              # Project name
        self.tasks: Dict[int, Task] = {}  # Store tasks by task_id
        self._next_task_id = 1        # Auto increment task ID

    # Add new task to project
    def add_task(self, title: str, desc: str, priority: int) -> Task:
        title = title.strip()
        desc = desc.strip()

        if not title:
            raise ValueError("Title required.")
        if not (1 <= priority <= 5):
            raise ValueError("Priority must be 1-5.")

        # Create Task object
        t = Task(self._next_task_id, title, desc, priority)

        # Store in dictionary
        self.tasks[t.task_id] = t

        # Increase ID counter
        self._next_task_id += 1

        return t

    # Change task status
    def move_task(self, task_id: int, new_status: str) -> None:
        if task_id not in self.tasks:
            raise KeyError("Task not found.")
        self.tasks[task_id].change_status(new_status)

    # List tasks with optional filtering and sorting
    def list_tasks(
        self, status: Optional[str], sorter: SortStrategy
    ) -> List[Task]:

        tasks = list(self.tasks.values())

        # Filter by status if provided
        if status:
            s = status.strip().upper()
            tasks = [t for t in tasks if t.status == s]

        # Apply sorting strategy
        return sorter.sort(tasks)


# TaskBoard class (main manager of projects)
class TaskBoard:
    def __init__(self):
        self.projects: Dict[str, Project] = {}

    # Create new project
    def create_project(self, project_id: str, name: str) -> None:
        project_id = project_id.strip()
        name = name.strip()

        if not project_id or not name:
            raise ValueError("Project ID and name required.")
        if project_id in self.projects:
            raise ValueError("Project ID already exists.")

        self.projects[project_id] = Project(project_id, name)

    # Get project by ID
    def get_project(self, project_id: str) -> Project:
        if project_id not in self.projects:
            raise KeyError("Project not found.")
        return self.projects[project_id]


# Function to choose sorting strategy
def choose_sorter() -> SortStrategy:
    ans = input("Sort by (priority/created): ").strip().lower()
    return SortByPriority() if ans == "priority" else SortByCreated()


# Main function
def main():
    board = TaskBoard()  # Create TaskBoard object

    while True:
        print("\n--- TaskBoard Menu ---")
        print("1) Create project")
        print("2) List projects")
        print("3) Add task to project")
        print("4) Move task status")
        print("5) List tasks (filter + sort)")
        print("6) Add tag to task")
        print("7) show task history")
        print("8) Exit")

        choice = input("Choose: ").strip()

        try:
            if choice == "1":
                pid = input("Project ID: ")
                name = input("project name")
                board.create_project(pid, name)
                print("Project created.")

            elif choice == "2":
                if not board.projects:
                    print("No projects.")
                else:
                    for pid, p in board.projects.items():
                        print(f"{pid}: {p.name} (tasks={len(p.tasks)})")

            elif choice == "3":
                pid = input("Project ID: ")
                p = board.get_project(pid)
                title = input("Task title: ")
                desc = input("Description: ")
                priority = int(input("Priority 1-5: "))
                t = p.add_task(title, desc, priority)
                print("Task added:", t.summary())

            elif choice == "4":
                pid = input("Project ID: ")
                p = board.get_project(pid)
                tid = int(input("Task ID: "))
                status = input("New status (TODO/DOING/DONE): ")
                p.move_task(tid, status)
                print("Status update.")

            elif choice == "5":
                pid = input("Project ID: ")
                p = board.get_project(pid)
                status = input("Filter status (TODO/DOING/DONE or blank): ").strip()
                status = status if status else None
                sorter = choose_sorter()
                tasks = p.list_tasks(status, sorter)

                if not tasks:
                    print("No tasks found.")
                else:
                    for t in tasks:
                        print(t.summary())

            elif choice == "6":
                pid = input("Project ID: ")
                p = board.get_project(pid)
                tid = int(input("Task ID: "))
                tag = input("Tag: ")

                if tid not in p.tasks:
                    raise KeyError("Task not found.")

                p.tasks[tid].add_tag(tag)
                print("Tag added.")

            elif choice == "7":
                pid = input("Project ID: ")
                p = board.get_project(pid)
                tid = int(input("Task ID: "))

                if tid not in p.tasks:
                    raise KeyError("Task not found.")

                t = p.tasks[tid]
                print(t.summary())

                if not t.history:
                    print("No history yet.")
                else:
                    for step, action, old, new in t.history:
                        print(f"{step}. {action}: {old} -> {new}")

            elif choice == "8":
                print("Goodbye.")
                break

            else:
                print("invalid Choice.")

        except Exception as e:
            print("Error:", e)


# Run only if file executed directly
if __name__ == "__main__":
    main()
