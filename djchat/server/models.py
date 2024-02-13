"""
Module: models.py
Description: Defines the database models for managing categories, servers, and channels in the application.

Classes:
    - Category: Represents a category for organizing servers.
    - Server: Represents a server entity.
    - Channel: Represents a channel within a server.

Functions:
    - category_icon_uplpoad_path: Generates the upload path for category icons.
    - channel_banner_upload_path: Generates the upload path for channel banners.
    - channel_icon_upload_path: Generates the upload path for channel icons.
"""

from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.dispatch import receiver

from .validators import validate_icon_image_size, validate_image_file_extension


def category_icon_uplpoad_path(instance, filename):
    """
    Generates the upload path for category icons.

    Parameters:
        instance (Category): The instance of the Category model.
        filename (str): The original filename of the uploaded file.

    Returns:
        str: The generated upload path.
    """
    return f"category/{instance.id}/category_icon/{filename}"


def channel_banner_upload_path(instance, filename):
    """
    Generates the upload path for channel banners.

    Parameters:
        instance (Channel): The instance of the Channel model.
        filename (str): The original filename of the uploaded file.

    Returns:
        str: The generated upload path.
    """
    return f"channal/{instance.id}/channel_banner/{filename}"


def channel_icon_upload_path(instance, filename):
    """
    Generates the upload path for channel icons.

    Parameters:
        instance (Channel): The instance of the Channel model.
        filename (str): The original filename of the uploaded file.

    Returns:
        str: The generated upload path.
    """
    return f"channal/{instance.id}/channel_icon/{filename}"


class Category(models.Model):
    """
    Represents a category for organizing servers.

    Attributes:
        name (str): The name of the category.
        description (str): The description of the category.
        icon (FileField): The icon associated with the category.
    """
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    icon = models.FileField(upload_to=category_icon_uplpoad_path, null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to delete existing icon file if updated.
        """
        if self.id:
            existing = get_object_or_404(Category, id=self.id)
            if existing.icon != self.icon:
                existing.icon.delete(save=False)
        super(Category, self).save(*args, **kwargs)

    @receiver(models.signals.pre_delete, sender="server.Category")
    def category_delete_files(sender, instance, **kwargs):
        """
        Deletes associated icon file when a category instance is deleted.
        """
        for field in instance._meta.fields:
            if field.name == "icon":
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)

    def __str__(self):
        return self.name


class Server(models.Model):
    """
    Represents a server entity.

    Attributes:
        name (str): The name of the server.
        owner (User): The owner of the server.
        category (Category): The category to which the server belongs.
        description (str): The description of the server.
        member (ManyToManyField): The members of the server.
    """
    name = models.CharField(max_length=100, null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="server_owner")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="server_category")
    description = models.CharField(max_length=100, null=True, blank=True)
    member = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name


class Channel(models.Model):
    """
    Represents a channel within a server.

    Attributes:
        name (str): The name of the channel.
        owner (User): The owner of the channel.
        topic (str): The topic of the channel.
        server (Server): The server to which the channel belongs.
        banner (ImageField): The banner image of the channel.
        icon (ImageField): The icon of the channel.
    """
    name = models.CharField(max_length=100, null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="channel_owner")
    topic = models.CharField(max_length=100)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name="channel_server")
    banner = models.ImageField(
        upload_to=channel_banner_upload_path, null=True, blank=True, validators=[validate_image_file_extension]
    )
    icon = models.ImageField(
        upload_to=channel_icon_upload_path,
        null=True,
        blank=True,
        validators=[validate_icon_image_size, validate_image_file_extension],
    )

    def save(self, *args, **kwargs):
        """
        Overrides the save method to perform additional actions before saving.
        """
        self.name = self.name.lower()
        if self.id:
            existing = get_object_or_404(Channel, id=self.id)
            if existing.icon != self.icon:
                existing.icon.delete(save=False)
            if existing.banner != self.banner:
                existing.banner.delete(save=False)

        super(Channel, self).save(*args, **kwargs)

    @receiver(models.signals.pre_delete, sender="server.Channel")
    def category_delete_files(sender, instance, **kwargs):
        """
        Deletes associated files when a channel instance is deleted.
        """
        for field in instance._meta.fields:
            if field.name == "icon" or field.name == "banner":
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)

    def __str__(self):
        return self.name
