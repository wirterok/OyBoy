from django.utils.translation import gettext_lazy as _

class VideoType:
    VIDEO = 'video'
    SHORT = 'short'
    STREAM = 'stream'

    CHOICES = (
        (VIDEO, _('Video')),
        (SHORT, _('Short')),
        (STREAM, _('Stream')),
    )