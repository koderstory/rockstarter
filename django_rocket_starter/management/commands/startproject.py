# django_rocket_starter/management/commands/startproject.py
from django.core.management.base import BaseCommand
import shutil
import os

class Command(BaseCommand):
    help = 'Start a new Django project with the provided template'

    def add_arguments(self, parser):
        parser.add_argument('destination', type=str, help='The directory where the project should be created')

    def handle(self, *args, **options):
        template_dir = os.path.join(os.path.dirname(__file__), '../../template')
        destination_dir = options['destination']

        try:
            shutil.copytree(template_dir, destination_dir, dirs_exist_ok=True)
            self.stdout.write(self.style.SUCCESS(f'Project started successfully in {destination_dir}.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
