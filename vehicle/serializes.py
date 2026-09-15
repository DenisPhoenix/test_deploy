from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Car, Milage, Moto
from .services import convert_currencies
from .validators import TitleValidator


class MilageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Milage
        fields = ("id", "milage", "year", "moto", "car")


class CarSerializer(serializers.ModelSerializer):
    last_milage = serializers.SerializerMethodField(read_only=True)
    # usd_price = serializers.SerializerMethodField(read_only=True)
    milage = MilageSerializer(many=True, read_only=True)

    @staticmethod
    def get_last_milage(obj):
        if obj.milage.all().first():
            return obj.milage.all().first().milage
        return 0

    # @staticmethod
    # def get_usd_price(obj):
    #     return convert_currencies(obj.amount)

    class Meta:
        model = Car
        fields = ("id", "title", "description", "last_milage", "milage", "price")


class MotoSerializer(serializers.ModelSerializer):
    last_milage = serializers.SerializerMethodField(read_only=True)
    milage = MilageSerializer(many=True, read_only=True)

    @staticmethod
    def get_last_milage(obj):
        if obj.milage.all().first():
            return obj.milage.all().first().milage
        return 0

    class Meta:
        model = Moto
        fields = ("id", "title", "description", "last_milage", "milage", "owner")


class MotoMilageSerializer(serializers.ModelSerializer):
    moto = MotoSerializer(read_only=True)

    class Meta:
        model = Milage
        fields = (
            "moto",
            "year",
            "milage",
        )


class MotoCreateMilageSerializer(serializers.ModelSerializer):
    milage = MilageSerializer(many=True, required=False)

    def create(self, validated_data):
        milage = validated_data.get("milage")
        moto = Moto.objects.create(**validated_data)
        if milage:
            for m in milage:
                Milage.objects.create(moto=moto, **m)
        return moto

    class Meta:
        model = Moto
        fields = ("title", "description", "milage")
        validators = [
            TitleValidator(field="title"),
            UniqueTogetherValidator(queryset=Moto.objects.all(), fields=["title", "description"]),
        ]


class CarCreateMilageSerializer(serializers.ModelSerializer):
    milage = MilageSerializer(many=True, required=False)

    def create(self, validated_data):
        milage = validated_data.get("milage")
        car = Car.objects.create(**validated_data)
        if milage:
            for m in milage:
                Milage.objects.create(car=car, **m)
        return car

    class Meta:
        model = Car
        fields = ("title", "description", "price", "milage")
        validators = [
            TitleValidator(field="title"),
            UniqueTogetherValidator(queryset=Car.objects.all(), fields=["title", "description"]),
        ]
