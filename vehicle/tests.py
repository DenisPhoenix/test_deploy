from django.db.models import Model
from rest_framework.test import APITestCase
from rest_framework import status

from vehicle.models import Car


class VehicleTestCase(APITestCase):

    def setUp(self):
        pass

    def test_create_car(self):
        """Тестирование создания машины"""

        data = {
            "title": "test",
            "description": "test",
        }

        response = self.client.post("/api/cars/", data=data)
        # проверка статус кода
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # проверка выводимых данных
        self.assertEqual(response.json(), {"title": "test", "description": "test", "milage": [], "price": "0.00"})

        # проверка создания записи в БД
        self.assertTrue(Car.objects.all())

    def test_list_car(self):
        """Тестирование вывода списка машин"""

        Car.objects.create(title="list test", description="list test")
        response = self.client.get("/api/cars/")

        # проверка статус кода
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # проверка выводимых данных
        self.assertEqual(response.json(), [{'id': 2, 'title': 'list test', 'description': 'list test', 'last_milage': 0, 'milage': [], "price": "0.00"}])
