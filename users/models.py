from datetime import datetime, timezone
from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=200, default=uuid4)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    was_used = models.BooleanField(default=False)

    @property
    def is_valid(self):
        timedelta = datetime.now(timezone.utc) - self.created_at
        return timedelta.days < 1 and not self.was_used
