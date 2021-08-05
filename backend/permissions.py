import re
from rest_framework import permissions
from .models import PickPair, PickSession


class IsPickSessionOwnerOrSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['PUT', 'POST'] and request.data:
            required_pick_session_owner = PickSession.objects.get(
                id=request.data['pick_session_id']
            ).user
            user_is_superuser = request.user.is_superuser
            return required_pick_session_owner == request.user or user_is_superuser
        else:
            return True


class IsPickPairOwnerOrSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['PUT', 'POST'] and request.data:
            required_pick_pair_owner = PickPair.objects.get(
                id=request.data['pick_pair_id']
            ).pick_session.user
            user_is_superuser = request.user.is_superuser
            return required_pick_pair_owner == request.user or user_is_superuser
        else:
            return True