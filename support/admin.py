from django.contrib import admin
from rangefilter.filters import DateTimeRangeFilter

from support.models import SupportTicket, ReplyToTicket
from support.tasks import ticket_status_changed


class ReplyToTicketInline(admin.TabularInline):
    model = ReplyToTicket
    extra = 0
    readonly_fields = ('issue',)
    can_delete = False


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    inlines = (ReplyToTicketInline,)
    list_filter = ('status', 'subject', ('created_at', DateTimeRangeFilter))
    search_fields = ('user__telegram_id', 'user__username')
    search_help_text = 'Please enter Username or Telegram ID of the User you want to show their tickets (leave empty for all Users)'
    ordering = ('-created_at',)
    readonly_fields = ('user', 'subject', 'issue', 'created_at',)
    list_select_related = ('user',)

    def save_model(self, request, obj: SupportTicket, form, change):
        old_ticket = SupportTicket.objects.select_related('user').get(pk=obj.id)
        if obj.status != old_ticket.status:
            ticket_status_changed.delay(
                telegram_id=old_ticket.user.telegram_id,
                ticket_id=old_ticket.id,
            )
        return super().save_model(request, obj, form, change)

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
