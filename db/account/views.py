from django.shortcuts import render
from django.db.models import Count, Q, OuterRef, Subquery
from django_filters.rest_framework import DjangoFilterBackend
from pkg_resources import require
from rest_framework import filters, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet 

from db.video.serializers import ViewSerializer, ChannelReportSerializer 
from db.video.models import ChannelReport
from db.video.models import View
from db.account.models import Profile, Subscription
from db.account.serializers import ProfileSerializer, SubscriptionSerializer
from utils.base import Utils
# Create your views here.


class ViewHistoryViewSet(ModelViewSet):
    model_class = View
    serializer_class = ViewSerializer
    queryset = model_class.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(profile=self.request.user)
 

class InitialView(APIView):
    def get(self, request, format=None):
        instance = Profile.objects.filter(id=request.user.id) \
            .annotate(
                subscriber_count=Subquery(
                    Subscription.objects.filter(profile=OuterRef("pk"))
                        .values("profile").annotate(count=Count("id")).values("count")), 
                subscribtion_count=Subquery(
                    Subscription.objects.filter(subscriber=OuterRef("pk")).values("subscriber")
                        .annotate(count=Count("id")).values("count")),
            ).first()
        return Response(ProfileSerializer(instance=instance).data)


class ProfileViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   GenericViewSet):
    
    model_class = Profile
    serializer_class = ProfileSerializer
    queryset = model_class.objects

    def get_queryset(self):
        return super().get_queryset() \
            .annotate(
                subscriber_count=Subquery(
                    Subscription.objects.filter(profile=OuterRef("pk"))
                        .values("profile").annotate(count=Count("id")).values("count")), 
                subscribtion_count=Subquery(
                    Subscription.objects.filter(subscriber=OuterRef("pk")).values("subscriber")
                        .annotate(count=Count("id")).values("count")),
                subscribed=Count("subscribers", filter=Q(subscribers__subscriber=self.request.user))
            )

    @action(detail=True, methods=["post"])
    def report(self, request, pk):
        creds = dict(offender_id=pk, reporter=request.user)
        qs = ChannelReport.objects.filter(**creds)
        if qs.exists():
            return Response(qs.update(text=request.data.get("text")))
        report = ChannelReport.objects.create(**creds, text=request.data.get("text"))
        return Response(ChannelReportSerializer(report).data)

    @action(detail=True, methods=["post"])
    def subscribe(self, request, pk):
        creds = {"profile_id": pk, "subscriber": request.user}
        qs = Subscription.objects.filter(**creds)
        if qs.exists():
            return Response(qs.delete())
        instance = Subscription.objects.create(**creds)
        return Response(SubscriptionSerializer(instance).data)