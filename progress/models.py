from django.db import models
from django.contrib.auth.models import User


class UserProgress(models.Model):
    CHAT_TYPE_CHOICES = [
        ('assistance', 'Language Learning Assistance'),
        ('quiz', 'Quiz Chat'),
        ('matching', 'Matching Chat'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    chat_type = models.CharField(max_length=20, choices=CHAT_TYPE_CHOICES)
    level = models.IntegerField(default=1)
    total_sessions = models.IntegerField(default=0)
    quiz_score_avg = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    last_activity = models.DateTimeField(auto_now=True)
    achievements = models.JSONField(blank=True, null=True)
    
    class Meta:
        unique_together = ['user', 'chat_type']
        ordering = ['-last_activity']

    def __str__(self):
        return f"{self.user.username} - {self.get_chat_type_display()} - Level {self.level}"
