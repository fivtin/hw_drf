## Домашняя работа
### 25.1 Права доступа в DRF

1. Установите зависимости
2. В каталоге __config__ проекта создайте файл ___.env___ (или переименуйте __.env.sample__) и установите необходимые значения переменных.
3. Выполните миграции командой: ___python3 manage.py migrate___
4. Загрузите данные в БД командой __python3 manage.py loaddata data.json__
5. Запустите сервер командой ___python3 manage.py runserver___

### Основные URL
- http://127.0.0.1:8000/users/api_register - регистрация пользователя
- http://127.0.0.1:8000/users/token - получение JWT токена
- http://127.0.0.1:8000/courses/ - API курсов через методы [GET, POST, PATCH, DELETE]
- http://127.0.0.1:8000/lessons/create/, http://127.0.0.1:8000/lessons/X/[,update,delete] - API уроков
