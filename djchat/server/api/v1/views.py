from rest_framework import viewsets
from rest_framework.response import Response

from ...models import Server
from .serializers import ServerSerializer, ChannelSerializer, CategorySerializer


class ServerListViewset(viewsets.ViewSet):
    permission_classes = ()
    authentication_classes = ()
    queryset = Server.objects.all()

    def list(self, request):
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")

        if category:

            self.queryset = self.queryset.filter(category__id=category)

        if qty:
            self.queryset = self.queryset[: int(qty)]

        serializer = ServerSerializer(self.queryset, many=True)

        return Response(serializer.data)
            