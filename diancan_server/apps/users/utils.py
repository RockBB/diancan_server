def jwt_response_payload_handler(token, user=None, request=None):

    return {
        'token': token,
        'id': user.id,
        'username': user.username,
        'money': user.money,
    }


from django.contrib.auth.backends import ModelBackend
from .models import User
from django.db.models import Q
import re

def get_user_by_account(account):
    try:
        # if re.match('^1[3-9]\d{9}$', account):
        #     user = User.objects.get(mobile=account)
        # else:
        #     user = User.objects.get(username=account)

        user = User.objects.get(Q(mobile=account) | Q(username=account))

    except User.DoesNotExist:

        user = None

    return user


class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):

        user = get_user_by_account(username)

        if isinstance(user,User) and user.check_password(password) and self.user_can_authenticate(user):
            return user
