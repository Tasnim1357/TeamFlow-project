from django.db import models
from django.contrib.auth import get_user_model
from teams.models import Team
# Create your models here.
User = get_user_model()


class Task(models.Model):
    team= models.ForeignKey(Team, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_by= models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tasks")
    assigned_to= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tasks")
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title