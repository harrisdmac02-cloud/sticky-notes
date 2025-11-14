from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=200, blank=False)  # Enforce required and max_length
    content = models.TextField(blank=False)  # Enforce required
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
