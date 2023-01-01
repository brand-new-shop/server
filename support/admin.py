from django.contrib import admin
from rangefilter.filters import DateTimeRangeFilter

from support.models import SupportSubject, SupportTicket


@admin.register(SupportSubject)
class SupportSubjectAdmin(admin.ModelAdmin):
    ordering = ('name',)


@admin.register(SupportTicket)
class SupportRequest(admin.ModelAdmin):
    list_filter = ('status', 'subject', ('created_at', DateTimeRangeFilter))
    search_fields = ('user__telegram_id', 'user__username')
    search_help_text = 'Please enter Username or Telegram ID of the User you want to show their tickets (leave empty for all Users)'
    ordering = ('-created_at',)
    readonly_fields = ('user', 'subject', 'issue', 'created_at',)
    list_select_related = ('user', 'subject')

    def has_add_permission(self, request):
        return False

    def get_rangefilter_created_at_title(self, request, field_path):
        return 'Created at'
