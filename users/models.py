from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.forms import ValidationError
from users.managers import CustomUsermanager
import re

class ConfirmationCode(models.Model):
    user = models.OneToOneField("CustomUser", on_delete=models.CASCADE, related_name='confirmation_code')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Код подтверждения для {self.user.email}"
    

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    objects = CustomUsermanager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def clean(self):
        super().clean()
        if self.is_superuser and not self.phone_number:
            raise ValidationError({
                'phone_number': 'Phone number is required for superuser.'
            })
        
        if self.phone_number:
            self.validate_phone_number()

    def validate_phone_number(self):
        pattern = r'^\+?[1-9]\d{1,14}$'
        if not re.match(pattern, self.phone_number):
            raise ValidationError({
            })

    def save(self, *args, **kwargs):
        self.full_clean()  # Вызывает clean() и валидацию
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email or ""
