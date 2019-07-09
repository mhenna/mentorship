from rest_framework import permissions
from rest_framework_jwt import utils
from jwt import DecodeError
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User


class IsAdmin(permissions.BasePermission):
    missing_token = {"detail": "Authentication credentials were not provided."}
    invalid_token = {"detail": "Error decoding signature."}
    permission_denied = {
        "detail": "You do not have permission to perform this action."}

    def has_permission(self, request, view):
        
       
        try:
            DecodedUser = utils.jwt_decode_handler(
                request.META.get('HTTP_AUTHORIZATION')
            )
           
           
            user = User.objects.get(email=DecodedUser['email'])
            if user.is_superuser:
                return True
            return False
        except DecodeError:
            if request.META.get('HTTP_AUTHORIZATION') is not None:
                raise AuthenticationFailed(self.invalid_token)
            else:
                raise AuthenticationFailed(self.missing_token)