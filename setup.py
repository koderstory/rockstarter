# setup.py
from setuptools import setup, find_packages

setup(
    name='django-rocket-starter',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'django>=3.0',
    ],
    entry_points={
        'console_scripts': [
            'django-rocket-starter = django_rocket_starter.management.commands.startproject:Command.handle',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A Django starter project template',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/aldyahsn/django-rocket-starter',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
