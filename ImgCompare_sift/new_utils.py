import json

from django.utils import timezone
from appserver.models import UserLogin
from django.contrib.auth.models import User, Group
from django.core import serializers

def update_user_login(user):
    user.userlogin_set.create(timestamp=timezone.now())
    user.save()

def jwt_response_payload_handler(token, user=None, request=None):
    update_user_login(user)
    print user , User.objects.filter(id=user.id)
    login_count = len(UserLogin.objects.filter(user=user))
    user_data = {}

    for usr in User.objects.filter(id=user.id):
        user_data['id'] = usr.id
        user_data['username'] = usr.username
        user_data['email'] = usr.email
        user_data['first_name'] = usr.first_name
        user_data['last_name'] = usr.last_name
        user_data['is_staff'] = usr.is_staff

    return {
        'token': token,
        'user': user_data,
        'user_group': [x.name for x in user.groups.all()],
        'login_count': login_count
    }