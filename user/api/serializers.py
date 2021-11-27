from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout, authenticate

User = get_user_model()


class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    password_confirmation = serializers.CharField()

    def validate(self, attrs):
        password = attrs.get("password")
        password_confirmation = attrs.get("password_confirmation")
        if password != password_confirmation:
            raise serializers.ValidationError("Both the Password Field did not match")


        return super().validate(attrs=attrs)

    def validate_email(self, value):
        qs = User.objects.filter(email=value)
        if qs.exists():
            raise serializers.ValidationError("Email is already taken")

        return value

    class Meta:
        fields = ["email", "password", "password_confirmation"]


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        password = attrs.get("password")
        email = attrs.get("email")

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Email and Password did not match")
        self.user = user

        return super().validate(attrs=attrs)

    def validate_email(self, value):
        qs = User.objects.filter(email=value)
        if not qs.exists():
            raise serializers.ValidationError("Email is not Found")

        return value

    class Meta:
        fields = ["email", "password",]


