from datetime import *
from django.utils import timezone

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import json
from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self) -> None:
        # создаем тестового пользователя

        self.user = User.objects.create(
            telegram_account='Ali_TrofImova',
            chat_id='986959236',
            is_staff=True,
            is_superuser=True
        )
        self.user.set_password('1234')
        self.user.save()

        # аутентифицируем пользователя
        self.client.force_authenticate(user=self.user)

    def test_habit_create(self):
        """ тестирование создания привычки """

        # отправляем запрос на аутентификацию пользователя
        response = self.client.post('/user/token/', {"telegram_account": "Ali_TrofImova", "password": "1234"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # задаем данные для создания привычки
        data_habit = {
            "place_habit": "доме",
            "get_habit": "отжимание",
            "period_habit": "Раз в два дня",
            "time_limit": 20,
            "reward_habit": "eat ",
            "time_habit": "17:12",
            "create_time": "2023-12-22"
        }

        # создаем привычку
        response = self.client.post(
            '/habit/create/',
            data=data_habit
        )
        # print(response)
        #
        # print(response.json())

        # проверяем ответ на создание привычки
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.data = datetime.now().date()

        self.assertEqual(
            response.json(),
            {'id': 4, 'place_habit': 'доме', 'time_habit': '17:12:00',
             'get_habit': 'отжимание', 'nice_habit': False,
             'associated_habit': None, 'reward_habit': 'eat', 'time_limit': 20,
             'is_public': False, 'create_time': self.data.isoformat(), 'period_habit': 'Раз в два дня', 'owner': 4}

        )

        # проверяем на существование объектов привычек
        self.assertTrue(
            Habit.objects.all().exists()
        )

    def test_list_habit(self):
        """ тестирование списка привычек """

        self.maxDiff = None

        # отправляем запрос на аутентификацию пользователя
        response = self.client.post('/user/token/', {"telegram_account": "Ali_TrofImova", "password": "1234"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # создаем тестовую привычку
        Habit.objects.create(
            owner=self.user,
            place_habit="доме",
            get_habit="отжимание",
            period_habit="Раз в два дня",
            time_limit=20,
            reward_habit="eat ",
            time_habit="17:12",
        )


        # получаем список привычек
        response = self.client.get(
            ''
        )

        # проверяем ответ на получение списка привычек
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.data = datetime.now().date()

        # проверяем ответ на соответствие сохраненных данных
        self.assertEqual(
            response.json(),
            [{'id': 5, 'place_habit': 'доме', 'time_habit': '17:12:00', 'get_habit': 'отжимание', 'nice_habit': False,
              'associated_habit': None, 'reward_habit': 'eat ', 'time_limit': 20,
              'is_public': True, 'create_time': self.data.isoformat(), 'period_habit': 'Раз в два дня', 'owner': 5}]
        )

    def test_detail_habit(self):
        """ тестирование информации о привычке """

        # отправляем запрос на аутентификацию пользователя
        response = self.client.post('/user/token/', {"telegram_account": "Ali_TrofImova", "password": "1234"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        #задаем данные для создания привычки
        habit = Habit.objects.create(
            owner=self.user,
            place_habit="доме",
            get_habit="отжимание",
            period_habit="Раз в два дня",
            time_limit=20,
            reward_habit="eat ",
            time_habit="17:12:00",
        )

        # запрашиваем информацию об одной привычк
        response = self.client.get(
            reverse('habits:habit_get', kwargs={'pk': habit.pk})
        )

        #print(response.json())

        # проверяем ответ на получение привычки
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.data = datetime.now().date()

        # # проверяем ответ на соответствие сохраненных данных
        self.assertEqual(
            response.json(),
            {'id': 3, 'place_habit': 'доме', 'time_habit': '17:12:00', 'get_habit': 'отжимание',
              'nice_habit': False, 'associated_habit': None, 'reward_habit': 'eat ', 'time_limit': 20,
              'is_public': True, 'create_time': self.data.isoformat(), 'period_habit': 'Раз в два дня', 'owner': 3}
        )
    #

    def test_change_habit(self):
        """ тестирование изменения привычки """

        # отправляем запрос на аутентификацию пользователя
        response = self.client.post('/user/token/', {"telegram_account": "Ali_TrofImova", "password": "1234"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # задаем данные для создания привычки
        habit = Habit.objects.create(
            owner=self.user,
            place_habit="доме",
            get_habit="отжимание",
            period_habit="Раз в два дня",
            time_limit=20,
            reward_habit="eat",
            time_habit="17:12:00",
        )

        # данные для изменения привычки
        data_habit_change = {
            "place_habit": "улице",
            "get_habit": "отжимание",
            "period_habit": "Раз в два дня",
            "time_limit": 15,
            "reward_habit": "eat",
            "time_habit": "18:00",
        }

        # получаем детали привычки
        response = self.client.patch(
            reverse('habits:habit_update', kwargs={'pk': habit.pk}),
            data=data_habit_change
        )

        # print(response.json())

        # проверяем ответ на получение привычки
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.data = datetime.now().date()

        # проверяем ответ на соответствие сохраненных данных
        self.assertEqual(
            response.json(),
            {'id': 1, 'place_habit': 'улице', 'time_habit': '18:00:00', 'get_habit': 'отжимание',
             'nice_habit': False, 'associated_habit': None, 'reward_habit': 'eat', 'time_limit': 15,
             'is_public': True, 'create_time': self.data.isoformat(), 'period_habit': 'Раз в два дня', 'owner': 1}
        )

    def test_delete_habit(self):
        """ тестирование удаления привычки """

        # отправляем запрос на аутентификацию пользователя
        response = self.client.post('/user/token/', {"telegram_account": "Ali_TrofImova", "password": "1234"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # задаем данные для создания привычки
        habit = Habit.objects.create(
            owner=self.user,
            place_habit="доме",
            get_habit="отжимание",
            period_habit="Раз в два дня",
            time_limit=20,
            reward_habit="eat",
            time_habit="17:12:00",
        )

        # получаем детали привычки
        response = self.client.delete(
            reverse('habits:habit_delete', kwargs={'pk': habit.pk})
        )

        # проверяем ответ на получение привычки
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


