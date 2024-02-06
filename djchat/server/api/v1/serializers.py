from rest_framework import serializers
from ...models import  Server, Category, Channel


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model =Category
        fields = "__all__"

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"