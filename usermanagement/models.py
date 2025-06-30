from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import uuid


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class UserOrganizationMixin(models.Model):
    user = models.ForeignKey(
        User,  # settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)ss",
        help_text="User who owns or created this record",
    )
    organization = models.ForeignKey(
        "usermanagement.Organization",
        on_delete=models.CASCADE,
        related_name="%(class)ss",
        help_text="Organization this record belongs to",
    )

    class Meta:
        abstract = True


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when created"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp when last updated"
    )

    class Meta:
        abstract = True
