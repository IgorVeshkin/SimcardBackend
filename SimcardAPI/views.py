import datetime
from http.client import HTTPResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

# Create your views here.

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import TariffPlan, Simcard
from .serializers import TariffPlanSerializer, SimcardSerializer, UserSerializer


class Index(APIView):
    def get(self, request):
        # Получаем все тарифы

        all_tariffs = TariffPlan.objects.all()

        tariff_serializer = TariffPlanSerializer(all_tariffs, many=True)

        # Получаем все симкарты

        all_simcards = Simcard.objects.all()

        simcard_serializer = SimcardSerializer(all_simcards, many=True)

        # Формируем ответ

        response = {
            'Message': 'If you see this message then Everything Works Fine!',
            'tariffs': tariff_serializer.data,
            'simcards': simcard_serializer.data,
        }

        return Response(response, status=status.HTTP_200_OK)


class NewSimcard(APIView):
    def post(self, request):
        print('IMEI пользователя:', request.data['IMEI'])

        currentTariff = TariffPlan.objects.get(id=request.data['TariffPlan'])

        data = request.data.copy()
        data['TariffPlan'] = currentTariff

        sim = Simcard.objects.create(**data)

        sim_serializer = SimcardSerializer(instance=sim)

        response = {
            'Message': 'Response from server is successful!',
            'Simcard': sim_serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)


class DeleteSimcard(APIView):
    def post(self, request):
        sim_id = request.data['id']

        Simcard.objects.get(id=sim_id).delete()

        response = {
            'Message': 'Simcard has been successfully deleted!',
        }
        return Response(response, status=status.HTTP_200_OK)


class UpdateSimcard(APIView):
    def post(self, request):

        # Получаем id симкарты
        sim_id = request.data['id']

        # Ищем запись по id

        try:
            update_sim = Simcard.objects.get(id=int(sim_id))
        except ObjectDoesNotExist:

            # Если не находим, то возвращаем следующий ответ в frontend

            response = {
                'error_message': 'Simcard wasn\'t found!'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        # Сохраняем данные из словаря запроса в запись

        # Обновляем запись
        for attr, value in request.data.items():

            # В случае если очередь дошла до TariffPlan необходимо по id получить сущность тарифного плана
            # и передать его как значение аттрибута

            if attr == 'TariffPlan':
                setattr(update_sim, attr, TariffPlan.objects.get(id=int(value)))
                continue

            setattr(update_sim, attr, value)

        # Обновляем поле даты и времени обновления записи
        update_sim.RecordUpdateTime = datetime.datetime.now()

        # Сохраняем изменения
        update_sim.save()

        # Возвращаем ответ об успешной работе

        response = {
            'Message': 'Simcard has been successfully updated!',
        }
        return Response(response, status=status.HTTP_200_OK)


class GetUser(APIView):
    def get(self, request):

        if request.user.is_anonymous:
            response = {
                'user': {
                    'username': 'AnonymousUser'
                },

            }

            return Response(response, status=status.HTTP_200_OK)

        response = {
            'user': UserSerializer(instance=request.user).data,

        }

        return Response(response, status=status.HTTP_200_OK)


class LoginUser(APIView):
    def post(self, request):
        # Получаем username и password из frontend-а
        username = request.data['username']
        password = request.data['password']
        try:
            found_user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            response = {
                'error_message': f'Неправильный логин'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        if not found_user.check_password(password):
            response = {
                'error_message': f'Неправильный пароль'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        if not found_user.is_authenticated:
            response = {
                'Message': f'Пользователь уже авторизован в системе',
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)

        user = authenticate(username=username, password=password)

        if not user:
            response = {
                'Message': f'Не удалось авторизовать пользователя',
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)

        login(request, user)

        response = {
            'Message': f'Пользователь был успешно авторизован',
            'user': UserSerializer(instance=user).data,
        }
        return Response(response, status=status.HTTP_200_OK)


class LogoutUser(APIView):
    def post(self, request):
        # Получаем username из frontend-а
        username = request.data['username']
        try:
            found_user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            response = {
                'error_message': f'Пользователь не найден'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        if found_user != request.user:
            response = {
                'error_message': f'Пользователь не находиться в текущей сессии'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        logout(request)

        response = {
            'Message': f'Пользователь успешно вышел из профиля',
        }
        return Response(response, status=status.HTTP_200_OK)


def front(request):
    context = { }
    return render(request, "index.html", context)
