from urllib import request
from rest_framework.viewsets import ModelViewSet
from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from utils.base import Utils
from django.db.models import Count, Q, OuterRef, Subquery

from . import models
from . import serializers
from .filterset import VideoFilterset, TagFilterset, CommentFilterset
from db.account.models import Subscription
# Create your views here.


class VideoViewSet(ModelViewSet):
    model_class = models.Video
    serializer_class = serializers.VideoSerializer
    queryset = model_class.objects.filter()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = VideoFilterset
    search_fields = ['name', 'profile__username']
    ordering_fields = ["id", "created_at", "view_count"]

    def get_queryset(self):
        profile = self.request.user
        qs = super().get_queryset() \
            .annotate(
                like_count=Count('like'),
                dislike_count=Count("dislike"),
                comment_count=Count("comment"),
                view_count=Count("view"),
                liked=Count("like", filter=Q(like__profile=profile)),
                favourited=Count("favourite", filter=Q(favourite__profile=profile))
            ).prefetch_related("profile", "tags")
        if not self.request.query_params.get("show_banned"):
            qs = qs.filter(banned=False, profile__banned=False)
        if not self.request.query_params.get("show_own", False):
            qs = qs.filter(~Q(profile=profile))
        if self.request.query_params.get("q", "") == "subscribtion":
            qs = qs.annotate(is_subscriber=Subquery(
                    Subscription.objects.filter(profile=OuterRef("profile"), subscriber=profile).values("subscriber")
                        .annotate(count=Count("id")).values("count"))
                ).filter(is_subscriber__gt=0)
        return qs
    
    @action(detail=True, methods=["post"])
    def like(self, request, pk):
        return Utils.toggle_view(pk, "video_id", request.user, model=models.Like, serializer=serializers.LikeSerializer)

    @action(detail=True, methods=["post"])
    def favourite(self, request, pk):
        return Utils.toggle_view(pk, "video_id", request.user, model=models.Favourite, serializer=serializers.FavouriteSerializer)

    @action(detail=True, methods=["post"])
    def view(self, request, pk):
        creds = dict(video_id=pk, profile=request.user)
        models.View.objects.filter(**creds).delete()
        view = models.View.objects.create(**creds)
        return Response(serializers.ViewSerializer(view).data)

    @action(detail=True, methods=["post"])
    def report(self, request, pk):
        creds = dict(video_id=pk, reporter=request.user)
        qs = models.VideoReport.objects.filter(**creds)
        if qs.exists():
            return Response(qs.update(text=request.data.get("text")))
        report = models.VideoReport.objects.create(**creds, text=request.data.get("text"))
        return Response(serializers.VideoReportSerializer(report).data)

    
class TagViewSet(ModelViewSet):
    model_class = models.Tag
    filterset_class = TagFilterset
    filter_backends = [DjangoFilterBackend]
    serializer_class = serializers.TagSerializer
    queryset = model_class.objects

    def get_queryset(self):
        return super().get_queryset().filter(
                ~Q(video__profile=self.request.user),
                video__profile__banned=False,
                video__banned=False
            ) \
            .values("title").annotate(count=Count("id")).order_by("-count")

    @action(detail=False, methods=["post"])
    def bulk(self, request):
        objects = [models.Tag(**x) for x in request.data.get("tags", [])]
        tags = models.Tag.objects.bulk_create(objects, ignore_conflicts=True)
        return Response(serializers.TagSerializer(tags, many=True).data)


class SearchHistoryViewSet(ModelViewSet):
    model_class = models.SearchHistory
    serializer_class = serializers.SearchSerializer
    queryset = model_class.objects
    search_fields = ["text"]

    # filterset_class = TagFilterset
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
        # TODO - add searched
        return super().get_queryset() \
            .values("text", "video_type") \
            .annotate(
                search_count=Count("id"),
                searched=Count("id", filter=Q(profile=self.request.user))
            ) \
            .order_by("-search_count")


class CommentViewSet(ModelViewSet):
    model_class = models.Comment
    serializer_class = serializers.CommentSerializer
    queryset = model_class.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CommentFilterset
    search_fields = ['name', 'profile__username']
    ordering_fields = ["id", "created_at"]

    def get_queryset(self):
        annotations = {
            "like_count": Count('likes'),
            "dislike_count": Count("dislikes")
        }
        return super().get_queryset().annotate(**annotations)


class FavouriteViewSet(ModelViewSet):
    model_class = models.Favourite
    serializer_class = serializers.FavouriteSerializer
    queryset = model_class.objects.all()


class LikeViewSet(ModelViewSet):
    model_class = models.Like
    serializer_class = serializers.LikeSerializer
    queryset = model_class.objects.all()


class DislikeViewSet(ModelViewSet):
    model_class = models.Dislike
    serializer_class = serializers.DislikeSerializer
    queryset = model_class.objects.all()


class ViewViewSet(ModelViewSet):
    model_class = models.View
    serializer_class = serializers.ViewSerializer
    queryset = model_class.objects.all()
