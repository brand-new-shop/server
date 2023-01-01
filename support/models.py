from django.db import models

from accounts.models import User


class SupportTicket(models.Model):
    STATUSES = (
        (1, 'Open'),
        (2, 'Pending'),
        (3, 'On Hold'),
        (4, 'Closed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.PositiveSmallIntegerField(choices=STATUSES, default=1)
    issue = models.TextField()
    answer = models.TextField(null=True, blank=True)

    def __str__(self):
        username = self.user.username
        if username is None:
            username = str(self.user.telegram_id)
        return f'@{username} - #{self.id} {self.subject}'
