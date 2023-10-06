from pkg_resources import require
from rest_framework import serializers

from .models import Profile, Subscription


class ProfileSerializer(serializers.ModelSerializer):
    subscriber_count = serializers.SerializerMethodField(read_only=True, required=False)
    subscribtion_count = serializers.SerializerMethodField(read_only=True, required=False)
    subscribed = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Profile
        fields = "__all__"
    
    def get_subscriber_count(self, obj):
        if subs := getattr(obj, "subscriber_count", None):
            return subs
        return 0
    
    def get_subscribtion_count(self, obj):
        if subs := getattr(obj, "subscribtion_count", None):
            return subs
        return 0

    def get_subscribed(self, obj):
        if subscribed := getattr(obj, "subscribed", None):
            return bool(subscribed)
        return False


class SubscriptionSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    subscriber = ProfileSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = ["profile", "subscriber"]

    