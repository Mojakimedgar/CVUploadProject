from django.contrib import admin
from .models import UserCV

@admin.register(UserCV)
class UserCVAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'email', 'skills', 'uploaded_file')
    search_fields = ('user__username', 'full_name', 'email')