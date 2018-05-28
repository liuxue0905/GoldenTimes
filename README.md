# GoldenTimes
GoldenTimes Python Django

## virtualenvs
If not install venv
```
$ apt-get install python3-venv
```
Create virtualenv
```
$ mkdir ~/.virtualenvs
$ python3 -m venv ~/.virtualenvs/djangodev
```
The final step in setting up your virtualenv is to activate it:
```
$ source ~/.virtualenvs/djangodev/bin/activate
```
If the source command is not available, you can try using a dot instead:
```
$ . ~/.virtualenvs/djangodev/bin/activate
```

## pip install

```
$ pip install django
$ pip install django-imagekit
$ pip install openpyxl
```

## manage

```
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver 0:8888
```
