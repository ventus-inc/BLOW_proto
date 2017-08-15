from django.db import models
from django.conf import settings


class WalletProfileManager(models.Manager):
    use_for_related_fields = True
    def get_wallet_num(self):
        return

class WalletProfile(models.Model):
    wallet_num = models.CharField(
        blank=True,
        null=True,
        max_length=40,)

    def get_wallet_num(self):
        users = self.wallet_num.all()
        return users.exclude(username=self.user.username)
    objects = WalletProfileManager()

# hoge = User.objects.first()
# User.objects.get_or_create()
