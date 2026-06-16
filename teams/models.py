from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Team(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teams")

    def __str__(self):
        return self.name
    

class TeamMember(models.Model):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("member", "Member"),
    )
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name = "members")
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name="team_memberships")   
    role =models.CharField(max_length=20, choices=ROLE_CHOICES, default="member") 

    def __str__(self):
        return f"{self.user.user_name} - {self.team.name} ({self.role})"