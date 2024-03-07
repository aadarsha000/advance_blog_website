from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    full_name = models.CharField(max_length=250, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to="user/avatar", blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    state = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    description = RichTextField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserFollowing(models.Model):
    user_id = models.ForeignKey(
        "account.CustomUser", related_name="following", on_delete=models.CASCADE
    )
    following_user_id = models.ForeignKey(
        "account.CustomUser", related_name="followers", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} is following {self.following_user_id}"
