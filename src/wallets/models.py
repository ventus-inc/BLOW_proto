from django.db import models
from django.conf import settings
#from accounts.models import UserProfile

class WalletProfileManager(models.Manager):
    use_for_related_fields = True

class WalletProfile(models.Model):
    wallet_num = models.CharField(
        blank=True,
        null=True,
        max_length=40,)

    objects = WalletProfileManager()

# hoge = User.objects.first()
# User.objects.get_or_create()
