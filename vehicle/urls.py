from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .apps import VehicleConfig
from .views import (
    CarViewSet,
    MilageCreatAPIView,
    MilageListAPIView,
    MotoCreateAPIView,
    MotoDestroyAPIView,
    MotoListAPIView,
    MotoMilageListAPIView,
    MotoRetrieveAPIView,
    MotoUpdateAPIView, MilageDestroyAPIView,
)

app_name = VehicleConfig.name

router = DefaultRouter()
router.register(r"cars", CarViewSet, basename="cars")

urlpatterns = [
    path("api/", include(router.urls)),
    path("moto/", MotoListAPIView.as_view(), name="moto-list"),
    path("moto/detail/<int:pk>/", MotoRetrieveAPIView.as_view(), name="moto-detail"),
    path("moto/new/", MotoCreateAPIView.as_view(), name="moto-create"),
    path("moto/update/<int:pk>/", MotoUpdateAPIView.as_view(), name="moto-update"),
    path("moto/delete/<int:pk>/", MotoDestroyAPIView.as_view(), name="moto-delete"),
    # milage
    path("milage/", MilageListAPIView.as_view(), name="milage-list"),
    path("milage/new/", MilageCreatAPIView.as_view(), name="milage-create"),
    path("milage/delete/<int:pk>/", MilageDestroyAPIView.as_view(), name="milage-delete"),
    path("moto/milage/", MotoMilageListAPIView.as_view(), name="moto-milage-list"),
]
