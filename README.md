django-project-template
========================

This is the Django project template that I typically use based on the one suggested from the authors of the Two Scoops of Django book ([here](https://github.com/twoscoops/django-twoscoops-project)). To create a new Django project using this layout simply run::

    $ django-admin.py startproject --template=https://github.com/mleonard87/django-project-template/archive/develop.zip --extension=py,md,html project_name

and then install the dependencies (ideally inside a virtualenv, see below)::

In development::

    $ pip install -r requirements/local.txt

For production::

    $ pip install -r requirements.txt

*note: We install production requirements this way because many Platforms as a
Services expect a requirements.txt file in the root of projects.*

In `project_name/project_name/settings` create a file called `secrets.json` with the following contents ammending the values as appropriate. You can generate a Django secret key [here](http://www.miniwebtool.com/django-secret-key-generator/)

    {
      "SECRET_KEY": "",
      "DATABASE_NAME": "",
      "DATABASE_USER": "",
      "DATABASE_HOST": "",
      "DATABASE_PORT": "",
      "DATABASE_PASSWORD": "",
      "EMAIL_HOST": "smtp.google.com",
      "EMAIL_HOST_USER": "",
      "EMAIL_HOST_PASSWORD": "", 
      "EMAIL_PORT": 587
    }


Development Environment
=======================

You have several options in setting up your working environment.  We recommend
using virtualenv to separate the dependencies of your project from your system's python environment.

Virtualenv
----------

First, make sure you are using virtualenv (http://www.virtualenv.org). Once
that's installed, create your virtualenv::

    $ virtualenv venv_name

You will also need to ensure that the virtualenv has the project directory
added to the path. Adding the project directory will allow `django-admin.py` to
be able to change settings using the `--settings` flag.
