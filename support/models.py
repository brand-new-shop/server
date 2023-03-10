from django.db import models

from accounts.models import User


class SupportTicket(models.Model):
    class Status(models.IntegerChoices):
        OPEN = (1, 'Open')
        PENDING = (2, 'Pending')
        ON_HOLD = (3, 'On Hold')
        CLOSED = (4, 'Closed')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.OPEN)
    issue = models.TextField(max_length=4096)
    answer = models.TextField(null=True, blank=True)

    def __str__(self):
        username = self.user.username
        if username is None:
            username = str(self.user.telegram_id)
        return f'@{username} - #{self.id} {self.subject}'


class ReplyToTicket(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE)
    issue = models.TextField(max_length=4096)
    answer = models.TextField(max_length=4096, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'reply'
        verbose_name_plural = 'replies'

    def __str__(self):
        return f'Reply to ticket #{self.ticket_id}'
