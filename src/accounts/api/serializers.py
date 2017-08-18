from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from rest_framework import serializers
from accounts.models import WalletProfile, UserProfile
User = get_user_model()

class UserDisplaySerializer(serializers.ModelSerializer):
    follower_count = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    wallet_num = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'follower_count',
            'url',
            'wallet_num',
        ]

    def get_follower_count(self, obj):
        user = UserProfile.objects.get(user=obj)
        # print(user.get_following().count())
        return user.get_following().count()

    def get_url(self, obj):
        return reverse_lazy("profiles:detail", kwargs={"username": obj.username})

    def get_wallet_num(self, obj):
        wallet = WalletProfile.objects.get(user=obj)
        return wallet.num
