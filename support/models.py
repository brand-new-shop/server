from django.db import models
from django.utils.text import Truncator

from accounts.models import User


class SupportSubject(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class SupportRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(SupportSubject, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_open = models.BooleanField(default=True)
    issue = models.TextField()
    answer = models.TextField(null=True, blank=True)

    def __str__(self):
        return Truncator(self.issue).words(num=10, truncate="...")
