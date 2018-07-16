from django.db import models
from datetime import datetime

# Create your models here.

class Todo(models.Model):
    COLUMN_CHOICES = (
        ('left', 'left'),
        ('middle', 'middle'),
        ('right', 'right')
    )

    title = models.CharField(max_length=200)
    text = models.TextField()
    column_id = models.CharField(
        max_length=6,
        choices=COLUMN_CHOICES,
        default='left'
    )
    created_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title
