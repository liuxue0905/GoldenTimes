# GoldenTimes
GoldenTimes Python Django

```
$ mkdir ~/.virtualenvs
$ python3 -m venv ~/.virtualenvs/djangodev
```
```
$ source ~/.virtualenvs/djangodev/bin/activate
```
If the source command is not available, you can try using a dot instead:
```
$ . ~/.virtualenvs/djangodev/bin/activate
```

```
$ pip install django
$ pip install sorl-thumbnail
$ pip install django-watermark
$ pip install openpyxl
```

```
$ python manage.py migrate
$ python manage.py makemigrations
$ python manage.py createsuperuser
$ python manage.py runserver 0:8888
```

django-watermark
```
$ python setup.py install
```