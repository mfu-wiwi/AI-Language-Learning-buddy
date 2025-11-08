from django.db import models
from django.contrib.auth.models import User
import uuid


class ChatSession(models.Model):
    CHAT_TYPE_CHOICES = [
        ('assistance', 'Language Learning Assistance'),
        ('quiz', 'Quiz Chat'),
        ('matching', 'Matching Chat'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    chat_type = models.CharField(max_length=20, choices=CHAT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_chat_type_display()} - {self.title}"


class ChatMessage(models.Model):
    SENDER_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    message_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(blank=True, null=True)  # For quiz scores, matching results, etc.

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
