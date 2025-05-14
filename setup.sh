#!/bin/bash
pip cache purge

pip install setuptools
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput