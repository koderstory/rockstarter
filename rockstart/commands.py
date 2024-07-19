# rockstart/commands.py
import shutil
import os

def copy_project_files():
    current_dir = os.path.dirname(__file__)
    template_dir = os.path.join(current_dir, 'myproject')
    target_dir = os.getcwd()

    try:
        shutil.copytree(template_dir, target_dir, dirs_exist_ok=True)
        print('Project files copied successfully.')
    except Exception as e:
        print(f'Error: {e}')
