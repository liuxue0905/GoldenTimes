# GoldenTimes
GoldenTimes Python Django


## 依赖
```shell script
$ sudo apt-get install libjpeg-dev libxml2-dev
```
```shell script
$ pip install pipreqs
$ pip install Pillow
```

```shell script
$ pipreqs --force ./
```

```shell script
$ pip install --no-cache-dir -r requirements.txt
```

```shell script
$ pip install --upgrade django -i https://pypi.douban.com/simple
```

## manage

```shell script
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
```

```shell script
$ python manage.py runserver 0:8000
```

```shell script
$ gunicorn -b 0:8000 GoldenTimes.wsgi
```

## 部署清单
```shell script
$ python manage.py check --deploy
```

## 部署
运行 collectstatic 管理命令:
```shell script
$ python manage.py collectstatic
```
这将会把静态目录下的所有文件拷贝至 STATIC_ROOT 目录。