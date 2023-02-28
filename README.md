# Table of Contents
1. [General informations](#info)<br>
2. [Requirements](#requirements)<br>
3. [Run code](#running)<br>

## General informations <a name="info"></a>
TBA

## Requirements <a name="requirements"></a>
 - System with Python 3.9
 - Docker (optional) - for running app in docker
 - All other requirements listed in requirements.txt.  To install run:
```shell
pip install requirements.txt
```

## Run code <a name="running"></a>
To run the code locally simply run following commands:<br>
```shell
 python manage.py migrate
 ```
This will create DB with all required tables<br>
```shell
 python manage.py loaddata tiers
 ```
This will load default initial values to database.<br>
```shell
 python manage.py createsuperuser
 ```
This will create first user (admin) for that django project.<br>
```shell
 python manage.py runserver 8080
```
This will run server locally<br>

