from django.contrib import admin
from .models import Agency


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'approved', 'created_at']
    list_filter = ['approved', 'created_at']
    search_fields = ['name', 'email', 'phone', 'city', 'state', 'country']
