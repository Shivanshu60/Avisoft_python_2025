from django.db import models

# Create your models here.
class Paragraph(models.Model):
    url = models.URLField(max_length=500)
    title = models.CharField(max_length=200, blank=True)  # Add title field
    content = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)


