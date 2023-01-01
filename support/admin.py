from django.contrib import admin

from support.models import SupportSubject, SupportRequest


@admin.register(SupportSubject)
class SupportSubjectAdmin(admin.ModelAdmin):
    ordering = ('name',)


@admin.register(SupportRequest)
class SupportRequest(admin.ModelAdmin):
    list_filter = ('status', 'subject')
    search_fields = ('issue',)
    search_help_text = 'Search in request\'s issue text'
    ordering = ('-created_at',)
    readonly_fields = ('user', 'subject', 'issue', 'created_at',)
    list_select_related = ('user', 'subject')

    def has_add_permission(self, request):
        return False
