# django_rocket_starter/management/commands/startproject.py
from django.core.management.base import BaseCommand
import shutil
import os

class Command(BaseCommand):
    help = 'Start a new Django project with the provided template'

    def handle(self, *args, **options):
        template_dir = os.path.join(os.path.dirname(__file__), '../../template')
        target_dir = os.path.abspath('.')

        try:
            shutil.copytree(template_dir, target_dir, dirs_exist_ok=True)
            self.stdout.write(self.style.SUCCESS('Project started successfully.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
