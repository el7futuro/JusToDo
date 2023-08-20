JusToDo
JusToDo - это легкое и эффективное приложение для управления задачами, разработанное на фреймворке Django, 
чтобы помочь пользователям лучше организовать свой повседневный список дел. 
В качестве вдохновения послужил известный слоган "Just Do It!".

Основные функции
Создание, редактирование и удаление целей
Организация целей в категориях и досках
Определение приоритетов целей
Установка дат выполнения 
Отслеживание статуса выполнения (незавершенный, в работе, выполнен)
Защита личных данных с помощью аутентификации (логин + пароль)

Установка
Для установки и запуска проекта следуйте инструкциям ниже:

Клонируйте репозиторий
git clone https://github.com/el7futuro/JusToDo.git
Установите зависимости
pip install -r requirements.txt
Запустите миграции
python manage.py migrate
Запустите сервер
python manage.py runserver
Приложение будет доступно в браузере по адресу http://127.0.0.1:8000.

