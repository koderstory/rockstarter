# rockstart/commands.py
import shutil
import os
import sys

def copy_project_files():
    current_dir = os.path.dirname(__file__)
    template_dir = os.path.join(current_dir, 'src')
    target_dir = os.getcwd()

    try:
        if os.path.exists(template_dir):
            for item in os.listdir(template_dir):
                s = os.path.join(template_dir, item)
                d = os.path.join(target_dir, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)
            print('Project files copied successfully.')
        else:
            print(f"Template directory {template_dir} does not exist.")
    except Exception as e:
        print(f'Error: {e}')

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "go":
        copy_project_files()
    else:
        print("Usage: rockstart go")
