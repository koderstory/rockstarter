import sys
from rockstart.commands import copy_project_files

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "go":
        copy_project_files()
    else:
        print("Usage: rockstart go")