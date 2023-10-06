from rest_framework.response import Response

class Utils(object):
    @staticmethod
    def toggle_view(pk, pk_name, profile, model, serializer):
        creds = {pk_name: pk, "profile": profile}
        qs = model.objects.filter(**creds)
        if qs.exists():
            return Response(qs.delete())
        instance = model.objects.create(**creds)
        return Response(serializer(instance).data)