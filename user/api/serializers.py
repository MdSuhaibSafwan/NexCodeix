from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout, authenticate
from ..models import UserVerificationOTP
from batches.helpers import get_next_batch_classes

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
            raise serializers.ValidationError("Email and Password did not match.")

        if not user.is_verified:
            UserVerificationOTP.objects.get_or_create(user=user, expired=False)
            raise serializers.ValidationError("An Email has been sent to you please verify that one.")

        self.user = user

        return super().validate(attrs=attrs)

    def validate_email(self, value):
        qs = User.objects.filter(email=value)
        if not qs.exists():
            raise serializers.ValidationError("Email is not Found")

        return value

    class Meta:
        fields = ["email", "password",]


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    next_batches_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone", "present_address", "permanent_address", "next_batches_count"]

    def get_next_batches_count(self, serializer):
        classes = get_next_batch_classes(serializer)
        return classes.count()


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        # fields = "__all__"
        exclude = ["active", "date_created", "last_updated", "last_login", "password", "superuser", "staff"]

