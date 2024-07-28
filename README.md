## Домашняя работа
### 26.1 Celery (DRF)

1. Установите зависимости
2. В каталоге __config__ проекта создайте файл ___.env___ (или переименуйте __.env-sample__) и установите необходимые значения переменных.
3. Выполните миграции командой: ___python3 manage.py migrate___
4. Загрузите данные в БД командой __python3 manage.py loaddata data.json__
5. Запустите сервер командой ___python3 manage.py runserver___
6. В отдельных окнах терминала выполните команды
    - __celery -A config worker -l INFO__ [-P eventlet] - дополнительный параметр для Windows
    - __celery -A config beat -l INFO__

### Задания
1. Настроен проект для работы с Celery и Celery-Beat (для выполнения периодических задач).
2. Добавлена асинхронная рассылка писем пользователям об обновлении материалов курса - __lms.tasks.send_email_for_course_update__
3. Добавлена периодическая задача блокирования неактивных более 30 дней пользователей - __lms.tasks.block_inactive_users__

### Основные URL
- http://127.0.0.1:8000/users/api_register - регистрация пользователя
- http://127.0.0.1:8000/users/token - получение JWT токена
- http://127.0.0.1:8000/courses/ - API курсов через методы [GET, POST, PATCH, DELETE]
- http://127.0.0.1:8000/lessons/create/, http://127.0.0.1:8000/lessons/X/[,update,delete] - API уроков
- http://127.0.0.1:8000/subscribe/ - POST-метод для подписки / отписки на обновления курса
- http://127.0.0.1:8000/users/courses/payment/ - POST-метод для создания платежа и получения ссылки на оплату курса
- http://127.0.0.1:8000/docs/, http://127.0.0.1:8000/swagger/, http://127.0.0.1:8000/redoc/ - документация для API
