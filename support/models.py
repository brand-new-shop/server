from django.db import models

from accounts.models import User


class SupportSubject(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class SupportRequest(models.Model):
    STATUSES = (
        (1, 'Open'),
        (2, 'Pending'),
        (3, 'On Hold'),
        (4, 'Closed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(SupportSubject, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.PositiveSmallIntegerField(choices=STATUSES, default=1)
    issue = models.TextField()
    answer = models.TextField(null=True, blank=True)

    def __str__(self):
        return Truncator(self.issue).words(num=10, truncate="...")
