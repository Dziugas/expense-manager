from django.http import Http404
from django.core.exceptions import PermissionDenied
from . models import CustomUser

def get_user_profile(user_id):
    try:
        user_profile = CustomUser.objects.get(id=user_id)
        return user_profile
    except CustomUser.DoesNotExist:
        raise Http404("User does not exist")

def check_if_request_user_is_profile_owner(request, user_profile):
    if not request.user == user_profile:
        raise PermissionDenied
