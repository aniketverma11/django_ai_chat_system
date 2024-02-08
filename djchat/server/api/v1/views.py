from django.db.models import Count

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed

from ...models import Server
from .serializers import ServerSerializer, ChannelSerializer, CategorySerializer


class ServerListViewset(viewsets.ViewSet):
    permission_classes = ()
    authentication_classes = ()
    queryset = Server.objects.all()

    def list(self, request):
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        by_serverId = request.query_params.get("by_serverid")
        with_num_member = request.query_params.get("with_num_member")

        if by_user or by_serverId and not request.user.is_authenticated:
            raise AuthenticationFailed()
        if with_num_member:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        if by_serverId:
            try:
                self.queryset = self.queryset.filter(id=by_serverId)
                if not self.queryset.exists():
                    raise ValidationError(detail=f"Server with id {by_serverId} not found")
            except ValueError:
                raise ValidationError(detail=f"Server with ID {by_serverId} not found")
        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if qty:
            self.queryset = self.queryset[: int(qty)]

        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)

        serializer = ServerSerializer(self.queryset, many=True, context={"num_members": with_num_member})

        return Response(serializer.data)
