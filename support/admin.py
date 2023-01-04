from django.contrib import admin
from rangefilter.filters import DateTimeRangeFilter

from support.models import SupportTicket, ReplyToTicket


class ReplyToTicketInline(admin.TabularInline):
    model = ReplyToTicket


@admin.register(SupportTicket)
class SupportTicket(admin.ModelAdmin):
    inlines = (ReplyToTicketInline,)
    list_filter = ('status', 'subject', ('created_at', DateTimeRangeFilter))
    search_fields = ('user__telegram_id', 'user__username')
    search_help_text = 'Please enter Username or Telegram ID of the User you want to show their tickets (leave empty for all Users)'
    ordering = ('-created_at',)
    readonly_fields = ('user', 'subject', 'issue', 'created_at',)
    list_select_related = ('user',)

    def has_add_permission(self, request):
        return False

    def get_rangefilter_created_at_title(self, request, field_path):
        return 'Created at'


@admin.register(ReplyToTicket)
class ReplyToTicketAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_at')
    ordering = ('created_at',)
    search_fields = ('ticket__id',)
    search_help_text = 'Search by Ticket ID or Reply ID'
    readonly_fields = ('issue',)
