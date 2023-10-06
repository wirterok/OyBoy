from django_filters import rest_framework as filters

from .models import Favourite, Video, Tag, Comment
from . import VideoType

class VideoFilterset(filters.FilterSet):
    tags = filters.BaseInFilter(field_name="tags__title", lookup_expr="in")
    profiles = filters.BaseInFilter(field_name="profile_id", lookup_expr="in")
    favourite_profiles = filters.BaseInFilter(field_name="favourite__profile_id", lookup_expr="in")
    exclude = filters.BaseInFilter(field_name="id", lookup_expr="in", exclude=True)
    dtype = filters.ChoiceFilter(choices=VideoType.CHOICES)

    class Meta:
        model = Video
        fields = ["tags", "dtype", "profile_id", "favourite"]


class CommentFilterset(filters.FilterSet):
    videos = filters.BaseInFilter(field_name="video_id", lookup_expr="in")

    class Meta:
        model = Comment
        fields = ["video_id"]


class TagFilterset(filters.FilterSet):
    video_type = filters.MultipleChoiceFilter(field_name="video__dtype", conjoined=True, choices=VideoType.CHOICES)

    class Meta:
        model = Tag
        fields = ["video_type"]