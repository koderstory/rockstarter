# rockstart/cli.py
import sys
from rockstart.commands import copy_project_files, deploy

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "go":
            copy_project_files()
        elif sys.argv[1] == "deploy" and len(sys.argv) > 2:
            domain_name = sys.argv[2]
            deploy(domain_name)
        else:
            print("Usage: rockstart go OR rockstart deploy [domain-name]")
    else:
        print("Usage: rockstart go OR rockstart deploy [domain-name]")
