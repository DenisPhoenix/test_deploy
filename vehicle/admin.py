from .models import Moto, Milage, Car
from django.contrib import admin


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(Moto)
class MotoAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(Milage)
class MilageAdmin(admin.ModelAdmin):
    list_display = ("car", "moto")
