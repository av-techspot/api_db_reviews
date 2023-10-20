# api_db_reviews
api_db_reviews - учебный групповой проект. Сервис собирает отзывы пользователей на произведения: "Фильмы", "Музыка", "Книги". Пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг.

### Стек:
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

### Как запустить проект:
- _Клонировать репозиторий и перейти в него в командной строке:_
```
git clone git@github.com:av-techspot/api_db_reviews.git
cd api_db_reviews
```
- _Cоздать и активировать виртуальное окружение:_
```
python3 -m venv env
source env/bin/activate
```
- Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
- Выполнить миграции:
```
python3 manage.py migrate
```
- Запустить проект:
```
python3 manage.py runserver
```

### Авторы:
Андрей Васильев, Артем Козин, Вера Фадеева
Выражаю благодарность моим соавторам.
