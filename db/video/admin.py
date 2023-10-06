from django.contrib import admin
from .models import (
    Like, Dislike, Favourite, 
    Video, Tag, View,
    Comment, CommentDislike, CommentLike, 
    VideoReport, ChannelReport
)
from django.db.models import Count

from db.account.models import Profile

# Register your models here.


# @admin.register(Like)
# class LikeAdmin(admin.ModelAdmin):
#     pass


# @admin.register(Dislike)
# class DislikeAdmin(admin.ModelAdmin):
#     pass


# @admin.register(Favourite)
# class FavouriteAdmin(admin.ModelAdmin):
#     pass


# @admin.register(View)
# class ViewAdmin(admin.ModelAdmin):
#     pass

    
class LikeInline(admin.TabularInline):
    model = Like


class TagInline(admin.TabularInline):
    model = Tag


class DislikeInline(admin.TabularInline):
    model = Dislike


class ViewInline(admin.TabularInline):
    model = View


class FavouriteInline(admin.TabularInline):
    model = Favourite


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    # inlines = [LikeInline, DislikeInline, ViewInline]
    inlines = [TagInline]
    list_display = ["name", "reports_count"]
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            reports_count=Count('reports'))
    
    def reports_count(self, obj):
        return obj.reports_count



class ProfileInline(admin.StackedInline):
    model = Profile


class VideoInline(admin.StackedInline):
    model = Video

    
@admin.register(VideoReport)
class VideoReportAdmin(admin.ModelAdmin):
    search_fields = ["text", "reporter__username", "video__name"]
    list_filter = ["video"]
    list_display = ["text", "video", "reporter"]
    # inlines = [VideoInline]

    
@admin.register(ChannelReport)
class ChannelReportAdmin(admin.ModelAdmin):
    search_fields = ["text", "offender__username", "reporter__username"]
    list_filter = ["offender"]
    list_display = ["text", "offender", "reporter"]
    # inlines = [ProfileInline]

# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     pass



# @admin.register(CommentLike)
# class CommentLikeAdmin(admin.ModelAdmin):
#     pass


# @admin.register(CommentDislike)
# class CommentDislikeAdmin(admin.ModelAdmin):
#     pass


# class CommentLikeInline(admin.TabularInline):
#     model = CommentLike


# class CommentDislikeInline(admin.TabularInline):
#     model = CommentDislike


# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     inlines = [CommentLikeInline, CommentDislikeInline]

