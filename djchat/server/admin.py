from django.contrib import admin

from djchat.server.models import Channel, Server, Category


class ChannelAdmin(admin.ModelAdmin):
    list_display=["id", "name", "owner", "topic", "server"]
    search_fields=("id", "name", "server")

class ServerAdmin(admin.ModelAdmin):
    list_display=["id", "name", "owner", "category", "description"]
    search_fields=("id", "name", "owner")

class CategoryAdmin(admin.ModelAdmin):
    list_display=["id", "name", "description"]
    search_fields=("id", "name")


admin.site.register(Channel, ChannelAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Category, CategoryAdmin)