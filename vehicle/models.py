from django.db import models
from users.models import User


class Car(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(max_length=100, verbose_name="Описание")
    amount = models.IntegerField(default=0, verbose_name="Цена")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Владелец машины")
    price = models.DecimalField(default=0, max_digits=12, decimal_places=2, verbose_name="Цена машины")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "машина"
        verbose_name_plural = "машины"


class Moto(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(max_length=100, verbose_name="Описание")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Владелец мотоцикла")
    price = models.DecimalField(default=0, max_digits=12, decimal_places=2, verbose_name="Цена мотоцикла")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "мотоцикл"
        verbose_name_plural = "мотоциклы"


class Milage(models.Model):
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name="milage", blank=True, null=True, verbose_name="Машина"
    )
    moto = models.ForeignKey(
        Moto, on_delete=models.CASCADE, related_name="milage", blank=True, null=True, verbose_name="Мотоцикл"
    )
    milage = models.PositiveIntegerField(verbose_name="Пробег")
    year = models.PositiveSmallIntegerField(verbose_name="Год регистрации")

    def __str__(self):
        car = self.car
        moto = self.moto
        year = self.year
        return f"{car if car else moto} - {year}"

    class Meta:
        verbose_name = "пробег"
        verbose_name_plural = "пробег"
        ordering = ("-year",)
