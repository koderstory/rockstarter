# setup.py
from setuptools import setup, find_packages

setup(
    name='rockstarter',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'rockstarter = rockstarter:main',
        ],
    },
    author='Koderstory',
    author_email='hello@koderstory.com',
    description='A simple tool to create django-ready project',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/koderstory/django-rockstarter',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
