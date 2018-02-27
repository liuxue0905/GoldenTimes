# GoldenTimes
GoldenTimes Python Django

## virtualenvs

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
$ pip install sorl-thumbnail
$ pip install django-watermark
$ pip install openpyxl
```

## manage

```
$ python manage.py migrate
$ python manage.py makemigrations
$ python manage.py createsuperuser
$ python manage.py runserver 0:8888
```

## django-watermark

```
$ python setup.py install
```