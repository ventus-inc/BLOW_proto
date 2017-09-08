from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.urls import reverse_lazy
from web3 import Web3, HTTPProvider, KeepAliveRPCProvider

import json
# Create your models here.

class UserProfileManager(models.Manager):
    use_for_related_fields = True

    def all(self):
        qs = self.get_queryset().all()
        try:
            if self.instance:
                qs = qs.exclude(user=self.instance)
        except:
            pass
        return qs

    def toggle_follow(self, user, to_toggle_user):
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        if to_toggle_user in user_profile.following.all():
            user_profile.following.remove(to_toggle_user)
            added = False
        else:
            user_profile.following.add(to_toggle_user)
            added = True
        return added

    def is_following(self, user, followed_by_user):
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        if created:
            return False
        if followed_by_user in user_profile.following.all():
            return True
        return False

    def recommended(self, user, limit_to=10):
        profile = user.profile
        following = profile.following.all()
        following = profile.get_following()
        qs = self.get_queryset().exclude(user__in=following).exclude(id=profile.id).order_by("?")[:limit_to]
        return qs


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='profile')
    following = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='followed_by')
    image = models.ImageField(upload_to='profile_image', blank=True)
    objects = UserProfileManager()

    def __str__(self):
        return str(self.user)

    def get_following(self):
        users = self.following.all()
        return users.exclude(username=self.user.username)

    def get_follow_url(self):
        return reverse_lazy("profiles:follow", kwargs={"username": self.user.username})

    def get_absolute_url(self):
        return reverse_lazy("profiles:detail", kwargs={"username": self.user.username})

    def get_buy_token_url(self):
        return reverse_lazy("tokens:buy_token", kwargs={"username": self.user.username})

    def get_sell_token_url(self):
        return reverse_lazy("tokens:sell_token", kwargs={"username": self.user.username})


class WalletProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        related_name='wallet')
    num = models.CharField(
        blank=True,
        null=True,
        max_length=40,)
    balance = models.BigIntegerField(
        default=0,
        null=False,
    )
    # TODO: 売却中トークンのマスターを取得
    selling_token = models.BigIntegerField(
        default=0,
        null=False,
    )

    def get_token_lot(self):
        contract_address = "0x6e0c7be2765df7b728f7bcea307696f27ff5ce78"
        web3 = Web3(KeepAliveRPCProvider(host='localhost', port='8545'))
        web3.personal.unlockAccount(self.num, self.user.username)
        f = open("transactions/abi.json", 'r')
        abi = json.loads(f.read())
        # TODO: トークンごとにアドレスを取得
        cnt = web3.eth.contract(abi, contract_address, "My")
        tokenlot = cnt.call().balanceOf(self.num)
        # print(tokenlot)
        return tokenlot

    def __str__(self):
        return self.num


def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    # print(instance)
    if created:
        new_profile = UserProfile.objects.get_or_create(user=instance)


post_save.connect(post_save_user_receiver, sender=settings.AUTH_USER_MODEL)
