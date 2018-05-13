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
$ pip install sorl-thumbnail
$ pip install openpyxl
$ pip install django-imagekit
```

### django-watermark
```
$ pip install django-watermark(deprecated)

$ pip install git+https://github.com/liuxue0905/django-watermark.git

$ git clone https://github.com/liuxue0905/django-watermark.git
$ python setup.py install
```

### django-imagekit
```
https://github.com/matthewwithanm/django-imagekit.git

$ pip install git+https://github.com/mmv/django-imagekit.git
http://miguelventura.pt/django-imagekit-watermarks.html
```

## manage

```
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver 0:8888
```
