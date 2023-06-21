JusToDo
Приложение - планировщик задач

Используемые модули: python3.9, Django, Postgres

1. Создаем приложение todolist
2. Выкладываем на Гитхаб
3. Создаем виртуальное окружение
4. Создаем зависимости
5. Настройка конфигурации. 
5.1. Устанавливаем библиотеку python-dotenv
5.2. Создайте файл .env, в котором храним настройки по умолчанию
5.3. В todolist/settings.py добавляем поддержку библиотеки и переносим параметры: SECRET_KEY и DEBUG в .env
6. Создаем приложение Core  и добавляем его в INSTALLED_APPS
7. Создаем кастомную модель пользователя которая наследуется от AbstractUser
8. Устанавливаем Postgres, создаем БД, добавляем суперюзера.
9. Добавляем переменную окружения DATABASE_URL в файл .env.
10. Создаем и применяем миграции
11. Настраиваем админ-меню
12. Запускаем все сервисы с помощью Docker Compose
13. Создаем образ приложения и отправляем его в репозиторий на Docker hub.
14. Настраиваем автоматическую сборку приложения
15. Настраиваем автоматический деплой приложения
16. Реализовываем регистрацию