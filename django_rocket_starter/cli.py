# django_rocket_starter/cli.py
import sys
from django.core.management import execute_from_command_line

def main():
    execute_from_command_line(['django-admin', 'start'] + sys.argv[1:])
