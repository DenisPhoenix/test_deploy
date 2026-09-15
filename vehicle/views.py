from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Car, Milage, Moto
from .paginators import VehiclePaginator
from .permissions import IsOwnerOrStaff
from .serializes import (
    CarCreateMilageSerializer,
    CarSerializer,
    MilageSerializer,
    MotoCreateMilageSerializer,
    MotoMilageSerializer,
    MotoSerializer,
)
from .tasks import check_milage


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == "create":
            return CarCreateMilageSerializer
        return CarSerializer


class MotoCreateAPIView(generics.CreateAPIView):
    serializer_class = MotoCreateMilageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_moto = serializer.save()
        new_moto.owner = self.request.user
        new_moto.save()


class MotoListAPIView(generics.ListAPIView):
    serializer_class = MotoSerializer
    queryset = Moto.objects.all()
    pagination_class = VehiclePaginator


class MotoRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = MotoSerializer
    queryset = Moto.objects.all()


class MotoUpdateAPIView(generics.UpdateAPIView):
    serializer_class = MotoCreateMilageSerializer
    queryset = Moto.objects.all()
    permission_classes = [IsOwnerOrStaff]


class MotoDestroyAPIView(generics.DestroyAPIView):
    queryset = Moto.objects.all()


class MilageCreatAPIView(generics.CreateAPIView):
    serializer_class = MilageSerializer

    def perform_create(self, serializer):
        new_milage = serializer.save()
        if new_milage.car:
            check_milage.delay(new_milage.car_id, "Car")
        else:
            check_milage.delay(new_milage.moto_id, "Moto")



class MilageListAPIView(generics.ListAPIView):
    serializer_class = MilageSerializer
    queryset = Milage.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("car", "moto")  # ?car=2
    ordering_fields = ("year",)  # ?ordering=year

class MilageDestroyAPIView(generics.DestroyAPIView):
    queryset = Milage.objects.all()


class MotoMilageListAPIView(generics.ListAPIView):
    serializer_class = MotoMilageSerializer
    queryset = Milage.objects.filter(moto__isnull=False)
