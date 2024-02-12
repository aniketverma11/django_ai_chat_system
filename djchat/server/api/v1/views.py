# Import necessary modules
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed

# Import models and serializers
from ...models import Server
from .serializers import ServerSerializer, ChannelSerializer, CategorySerializer


# Define a viewset for listing servers
class ServerListViewset(viewsets.ViewSet):

    # Set permissions and authentication classes
    permission_classes = ()
    authentication_classes = ()

    # Define the initial queryset
    queryset = Server.objects.all()

    # Define the list method to handle GET requests
    def list(self, request):
        
        # Extract query parameters from the request
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        by_serverId = request.query_params.get("by_serverid")
        with_num_member = request.query_params.get("with_num_member")

        # Check authentication if filtering by user or server ID
        if by_user or by_serverId and not request.user.is_authenticated:
            raise AuthenticationFailed()

        # Annotate the queryset with the number of members if requested
        if with_num_member:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        # Filter the queryset by server ID if provided
        if by_serverId:
            try:
                self.queryset = self.queryset.filter(id=by_serverId)
                if not self.queryset.exists():
                    raise ValidationError(detail=f"Server with id {by_serverId} not found")
            except ValueError:
                raise ValidationError(detail=f"Server with ID {by_serverId} not found")

        # Filter the queryset by category if provided
        if category:
            self.queryset = self.queryset.filter(category__name=category)

        # Limit the queryset by quantity if provided
        if qty:
            self.queryset = self.queryset[: int(qty)]

        # Filter the queryset by user if requested
        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)

        # Serialize the queryset and return the response
        serializer = ServerSerializer(self.queryset, many=True, context={"num_members": with_num_member})
        return Response(serializer.data)
