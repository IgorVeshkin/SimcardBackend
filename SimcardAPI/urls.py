from django.urls import path

from .views import Index, NewSimcard, DeleteSimcard, UpdateSimcard, front, GetUser, LoginUser, LogoutUser

urlpatterns = [
    # CRUD-запросы приложения
    path('get-data/', Index.as_view(), name='index'),
    path('new-simcard/', NewSimcard.as_view(), name='new_simcard'),
    path('delete-simcard/', DeleteSimcard.as_view(), name='delete_simcard'),
    path('update-simcard/', UpdateSimcard.as_view(), name='update_simcard'),

    # Тестовый фронт главной страницы
    path("", front, name="front"),

    # Тестовый фронт страница логирования
    path("login/", front, name="front-login"),

    # Ссылка по настройке билда react js внутри проекта Django
    # https://dev.to/nagatodev/how-to-connect-django-to-reactjs-1a71?ysclid=lzubg61kp2646907811

    # Получение данных текущего авторизированного пользователя
    path('check-user/', GetUser.as_view(), name="check_user"),
    # Запрос-проверки логирования пользователя
    path('login-user/', LoginUser.as_view(), name='login_user'),
    # Запрос-проверки для выхода из текущей учетной записи пользователя
    path('logout-user/', LogoutUser.as_view(), name='logout'),

]
