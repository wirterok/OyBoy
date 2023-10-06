from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class CustomAuthBackend(BaseBackend):

    def get_user(self, user_id):
        try:
          return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


    def authenticate(self, request, username, password, **kwargs):
        try:
            user = User.objects.get(
                Q(username=username) | Q(email=username)
            )
            
        except User.DoesNotExist:
            return None

        return user if user.check_password(password) else None