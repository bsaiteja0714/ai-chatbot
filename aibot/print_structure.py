import os

EXCLUDE_DIRS = {'.venv', '__pycache__', 'node_modules', '.git'}

def print_structure(folder, prefix=""):
    items = [i for i in os.listdir(folder) if i not in EXCLUDE_DIRS]
    for index, item in enumerate(sorted(items)):
        path = os.path.join(folder, item)
        connector = "├── " if index < len(items) - 1 else "└── "
        print(prefix + connector + item)
        if os.path.isdir(path):
            extension = "│   " if index < len(items) - 1 else "    "
            print_structure(path, prefix + extension)

if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    print_structure(root)
