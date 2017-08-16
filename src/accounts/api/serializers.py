from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from rest_framework import serializers

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
        #print(obj.username)
        return 0

    def get_follower_count(self, obj):
        return 0

    def get_url(self, obj):
        return reverse_lazy("profiles:detail", kwargs={"username": obj.username})

    def get_wallet_num(self, obj):
        return hasattr(obj, 'wallet') and self.car is not None
