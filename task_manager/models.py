from django.db import models
from firstapp.models import Auth  # Import the Auth model

class TaskCreation(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        Auth,                          # Reference to firstapp's Auth model
        on_delete=models.CASCADE,      # What happens when Auth user is deleted
        related_name='tasks'           # Access tasks from Auth: user.tasks.all()
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class TaskUpdated(models.Model):
    # ForeignKey to TaskCreation (uses TaskCreation's PK)
    task = models.ForeignKey(
        TaskCreation,
        on_delete=models.CASCADE,
        related_name='updates'  # Access updates: task.updates.all()
    )
    updated_by = models.ForeignKey(
        Auth,
        on_delete=models.CASCADE,
        related_name='updates_made'
    )
    
    update_description = models.TextField()
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Update on {self.task.title} at {self.updated_at}"
    
