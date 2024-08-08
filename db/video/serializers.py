from rest_framework import serializers

from db.account.serializers import ProfileSerializer

from .models import Tag, VideoReport, ChannelReport, View, Like, Dislike, Favourite, Video, Tag, Comment, SearchHistory, CommentLike, CommentDislike


class ChannelReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelReport
        fields = "__all__"
        

class VideoReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoReport
        fields = "__all__"
        

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["title", "description"]


class ViewSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = View
        fields = ["profile", "video_id"]


class LikeSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ["profile", "video_id"]


class DislikeSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = Dislike
        fields = ["profile", "video_id"]


class FavouriteSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = Favourite
        fields = ["profile", "video_id"]


class SearchSerializer(serializers.ModelSerializer):
    searches = serializers.SerializerMethodField(read_only=True)
    searched = serializers.SerializerMethodField(read_only=True)
 
    def get_searches(self, obj):
        if likes := getattr(obj, "search_count", None):
            return likes
        return 0

    def get_searched(self, obj):
        if isinstance(obj, dict) and (searched := obj.get("searched", None)):
            return bool(searched)
        return False

    class Meta:
        model = SearchHistory
        extra_kwargs = {'profile': {'write_only': True}}
        fields = "__all__"


class VideoSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    tags = TagSerializer(many=True, required=False)
    likes = serializers.SerializerMethodField(read_only=True)
    dislikes = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    liked = serializers.SerializerMethodField(read_only=True)
    favourited = serializers.SerializerMethodField(read_only=True)
    views = serializers.SerializerMethodField(read_only=True)
    profile_id = serializers.IntegerField()

    class Meta:
        model = Video
        fields = "__all__"
    
    def get_liked(self, obj):
        if liked := getattr(obj, "liked", None):
            return bool(liked)
        return False

    def get_favourited(self, obj):
        if favourited := getattr(obj, "favourited", None):
            return bool(favourited)
        return False
    
    def get_likes(self, obj):
        if likes := getattr(obj, "like_count", None):
            return likes
        return 0

    def get_comments(self, obj):
        if comments := getattr(obj, "comment_count", None):
            return comments
        return 0

    def get_dislikes(self, obj):
        if dislikes := getattr(obj, "dislike_count", None):
            return dislikes
        return 0

    def get_views(self, obj):
        if views := getattr(obj, "view_count", None):
            return views
        return 0


class CommentSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    dislikes = serializers.SerializerMethodField(read_only=True)
    
    profile_id = serializers.IntegerField(write_only=True)
    video_id = serializers.IntegerField()
    # parent_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Comment
        # exclude = ["video"]
        fields = ["name", "description", "likes", "dislikes", "parent",
                  "video_id", "video", "profile", "profile_id"]

    def get_likes(self, obj):
        if likes := getattr(obj, "like_count", None):
            return likes
        return 0

    def get_dislikes(self, obj):
        if dislikes := getattr(obj, "dislike_count", None):
            return dislikes
        return 0

class CommentLikeSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = CommentLike
        fields = ["profile", "comment_id"]


class CommentDislikeSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = CommentDislike
        fields = ["profile", "comment_id"]
