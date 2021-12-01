from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.decorators import api_view, permission_classes
from . import serializers
from . import permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(http_method_names=["POST", ])
def login_api_view(request):
    data = request.data
    serialized = serializers.UserLoginSerializer(data=data)
    serialized.is_valid(raise_exception=True)

    user = serialized.user
    token_obj, created = Token.objects.get_or_create(user=user)
    status_data = {}
    status_data["token"] = token_obj.key
    status_data["status"] = "200 | success"
    
    return Response(status_data, status=status.HTTP_200_OK)


@api_view(http_method_names=["POST", ])
def registration_api_view(request):
    data = request.data
    serialized = serializers.UserRegistrationSerializer(data=data)
    serialized.is_valid(raise_exception=True)

    email = serialized.validated_data.get("email")
    pw = serialized.validated_data.get("password")
    
    user = User(email=email)
    user.set_password(pw)
    user.save()
    
    token_obj, created = Token.objects.get_or_create(user=user)
    status_data = {}
    status_data["token"] = token_obj.key
    status_data["status"] = "201 | created"
    status_data["email"] = str(user.email)

    return Response(status_data, status=status.HTTP_200_OK)


class UserProfileAPIView(RetrieveAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticatedAndVerified, ]

    def get_object(self):
        return self.request.user

