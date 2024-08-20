# setup.py
from setuptools import setup, find_packages

setup(
    name='rockstarter',
    version='0.1.4',
    packages=find_packages(),
    install_requires=[
        'Django>=4.2.15',
        'asgiref==3.8.1',
        'django-environ==0.11.2',
        'sqlparse==0.5.1',
        'whitenoise==6.7.0',
        'gunicorn==23.0.0'
    ],
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
