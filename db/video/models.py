from enum import unique
from django.db import models
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey
from db.account.models import BaseModel
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.

models.Q

from . import VideoType

class Video(BaseModel):
    profile = models.ForeignKey("account.Profile", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=524)
    description = models.CharField(max_length=128, null=True, blank=True)
    dtype = models.CharField(max_length=64, choices=VideoType.CHOICES)

    banner = models.ImageField(upload_to='image/', null=True, blank=True)
    video = models.FileField(upload_to='video/', null=True, blank=True)
    banned = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.name


class Tag(BaseModel):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=524, null=True)
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True, related_name="tags")

    def __str__(self) -> str:
        return self.title

    class Meta:
        unique_together = ('title', 'video')


class SearchHistory(BaseModel):
    text = models.CharField(max_length=254)
    video_type = models.CharField(max_length=64, choices=VideoType.CHOICES)
    profile = ForeignKey("account.Profile", on_delete=models.CASCADE)
    # TODO - user

    def __str__(self) -> str:
        return self.text


class Like(BaseModel):
    profile = ForeignKey("account.Profile", on_delete=models.SET_NULL, null=True)
    video = ForeignKey(Video, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.profile.username + "|" + self.video.name


class Dislike(BaseModel):
    profile = ForeignKey("account.Profile", on_delete=models.SET_NULL, null=True)
    video = ForeignKey(Video, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.profile.username + "|" + self.video.name

    class Meta:
        unique_together = ("profile", "video")


class View(BaseModel):
    profile = ForeignKey("account.Profile", on_delete=models.SET_NULL, null=True)
    video = ForeignKey(Video, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.profile.username + "|" + self.video.name

    class Meta:
        unique_together = ("profile", "video")


class Favourite(BaseModel):
    profile = ForeignKey("account.Profile", on_delete=models.CASCADE)
    video = ForeignKey(Video, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.profile.username + "|" + self.video.name

    class Meta:
        unique_together = ("profile", "video")


class Comment(BaseModel, MPTTModel):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512, null=True, blank=True)
    profile = models.ForeignKey("account.Profile", on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self) -> str:
        return self.name


class CommentLike(BaseModel):
    profile = ForeignKey("account.Profile", on_delete=models.SET_NULL, null=True)
    comment = ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes")

    def __str__(self) -> str:
        return self.profile.username + "|" + self.comment.name

    class Meta:
        unique_together = ("profile", "comment")


class CommentDislike(BaseModel):
    profile = ForeignKey("account.Profile", on_delete=models.SET_NULL, null=True)
    comment = ForeignKey(Comment, on_delete=models.CASCADE, related_name="dislikes")

    def __str__(self) -> str:
        return self.profile.username + "|" + self.comment.name

    class Meta:
        unique_together = ("profile", "comment")


class VideoReport(BaseModel):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="reports")
    reporter = ForeignKey("account.Profile", on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    
    def __str__(self) -> str:
        return self.video.name + "|" + self.text[:50]
    

class ChannelReport(BaseModel):
    offender = models.ForeignKey("account.Profile", on_delete=models.CASCADE, related_name="reports")
    reporter = ForeignKey("account.Profile", on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    
    def __str__(self) -> str:
        return self.offender.username + "|" + self.text[:100]
