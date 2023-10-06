from django.contrib import admin
from .models import Profile, Subscription
from db.video.admin import VideoInline, ViewInline, FavouriteInline, LikeInline, DislikeInline, Video
from django.db.models import Count
# Register your models here.

# @admin.register(Subscription)
# class SubscriptionAdmin(admin.ModelAdmin):
#     pass

class SubscriptionInline(admin.TabularInline):
    model = Subscription
    fk_name = "subscriber"
    

@admin.register(Profile)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ["username", "reports_count"]
    inlines = [SubscriptionInline, VideoInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            reports_count=Count('reports'))
    
    def reports_count(self, obj):
        return obj.reports_count