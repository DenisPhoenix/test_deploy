from rest_framework.permissions import BasePermission


class IsOwnerOrStaff(BasePermission):
    def has_permission(self, request, view):
        # проверка на менеджера
        if request.user.is_staff:
            return True

        # Проверка на владельца объекта
        return request.user == view.get_object().owner
