from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields.related import ForeignKey
from django.utils.translation import gettext_lazy as _

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Profile(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    description = models.CharField(max_length=524, null=True, blank=True)
    avatar = models.ImageField(upload_to="images/", null=True, blank=True)
    banned = models.BooleanField(default=False)
    full_name = models.CharField(max_length=256, null=True, blank=True)
    
    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = []
    
    def __str__(self) -> str:
        return self.username


class Subscription(models.Model):
    subscriber = models.ForeignKey('account.Profile', on_delete=models.CASCADE, related_name="subscribtions")
    profile = models.ForeignKey('account.Profile', on_delete=models.CASCADE, related_name="subscribers")
