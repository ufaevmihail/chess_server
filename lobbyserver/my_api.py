from rest_framework import serializers
from .models import *
from lobbychessserver.settings import SECRET_KEY
from django.http import HttpResponse
import jwt

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        exclude=[]

class UserSerializer(serializers.ModelSerializer):
    account = AccountSerializer(required=True)
    class Meta:
        model=User
        fields=('username','email','account')


def jwt_required(f):
    def inner(request,*args):
        try:
            request.payload=jwt.decode(request.headers['token'],SECRET_KEY,algorithms=["HS256"])
            return f(request,*args)
        except (jwt.InvalidTokenError, jwt.DecodeError) as exc:
            return HttpResponse(status=401)
    return inner