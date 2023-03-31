from rest_framework.permissions import IsAdminUser,BasePermission


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

class Is_state_user(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type=='2')



class Is_block_user(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type=='3')



class Is_stdent(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return (request.user and request.user.user_type=='4')


from .models import Block_allocation
from rest_framework import permissions
from datetime import datetime, time

class LimitedTimeUpdatePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Define the allowed update time interval
        allowed_update_start = time(hour=9, minute=0)
        allowed_update_end = time(hour=17, minute=0)

        # Check the current time
        now = datetime.now().time()
        return allowed_update_start <= now <= allowed_update_end
    
from rest_framework.permissions import BasePermission

class IsAllocatedToBlock(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.Block_allocation.filter(user=request.user.id).exists()
