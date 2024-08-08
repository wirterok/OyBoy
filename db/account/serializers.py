from pkg_resources import require
from rest_framework import serializers

from .models import Profile, Subscription


class ProfileSerializer(serializers.ModelSerializer):
    subscriber_count = serializers.SerializerMethodField(read_only=True, required=False)
    subscribtion_count = serializers.SerializerMethodField(read_only=True, required=False)
    subscribed = serializers.SerializerMethodField(read_only=True)
    # user_permissions = serializers.ListField(write_only=True)

    class Meta:
        model = Profile
        # exclude = ["user_permissions"]
        fields = "__all__"
        extra_kwargs = {'user_permissions': {'write_only': True}}

    
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

    
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Profile
        fields = ['username', 'email', 'password', 'is_active']

    def create(self, validated_data):
        user = Profile(
            username = validated_data['username'],
            email = validated_data['email'],
            is_active = validated_data['is_active'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    