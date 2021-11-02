from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):

    def create_user(self, email, password, is_active=True, is_superuser=True, is_staff=True):
        if not email:
            raise ValidationError("Users should always have an Email...")

        if not password:
            raise ValidationError("User Should Have a Password...")

        email = self.normalize_email(email=email)
        user_obj = self.model(
            email=email, active=is_active, superuser=is_superuser
        )
        user_obj.staff=is_staff
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None, is_active=True, is_superuser=False, 
                        is_staff=True ):
        """
        THIS RUNS TO CREATE STAFF USER...
        """
        return self.create_user(
            email,
            password,
            is_active,
            is_superuser,
            is_staff
        )


    def create_superuser(self, email, password=None, is_active=True, is_superuser=True, 
                        is_staff=True ):
        """
        THIS RUNS WHEN TO CREATE SUPER USER...
        """
        return self.create_user(
            email,
            password,
            is_active,
            is_superuser,
            is_staff
        )


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=25, null=True)

    permanent_address = models.TextField(null=True, blank=True)
    present_address = models.TextField(null=True, blank=True)

    verified = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    superuser = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELD = [] # Can Explicitely set that but email, USERNAME_FIELD and password are set by default

    def get_full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"

    def get_short_name(self):
        return self.middle_name

    def has_perm(self, perm, obj=None):
        if self.is_active:
            return True

        return False

    def has_module_perms(self, app_label):
        if not self.is_active:
            return False

        if self.is_superuser or self.is_staff:
            return True

        return False

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_superuser(self):
        return self.superuser
    
    @property
    def is_active(self):
        return self.active

    def is_verified(self):
        return self.verified

