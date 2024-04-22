
Running Django is easy, but deploying it to production is another story. With the Django project template, we don't need to worry about deployment. We can focus on developing the logic of the apps rather than fixing various server configurations.

Instead of serving static and media file using Nginx, this template uses Whitenoise for static file and boto3 to serve media files in S3 servers.

Why we need  to serve media file in S3 instead of local directory? Because when we develop the code in development mode we can still use production media files

## Features

What are the features included in the project template?

- **Django Environ**
    Python package that allows you to use Twelve-factor methodology to configure your Django application with environment variables.

- **Django Storages with boto3**
    Boto3 is the Amazon Web Services (AWS) Software Development Kit (SDK) for Python, which allows Python developers to write software that makes use of services like Amazon S3 and Amazon EC2

- **Django WhiteNoise**
    WhiteNoise is pretty efficient to serve static files

- **Django Admin Interfaces**
    Beautiful default django-theme


## Installation

1. Download template

```
 wget https://github.com/aldyahsn/django-template/blob/master/template.zip
```

2. Unzip the downloaded file into a directory named project_name

```
unzip django-template.zip -d project_name
```

3. Remove the ZIP file after extraction

```
rm django-template.zip
```

