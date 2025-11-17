from django.db import models

class Note(models.Model):
    """
    Model representing a sticky note with title and content.
    
    Fields:
        title (CharField): Short heading for the note (max 200 chars).
        content (TextField): Main body of the note.
        created_at (DateTimeField): Timestamp when note is created (auto-set).
        updated_at (DateTimeField): Timestamp when note is last updated (auto-set).
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
