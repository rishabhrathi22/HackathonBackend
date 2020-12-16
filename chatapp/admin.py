from django.contrib import admin
from .models import Chat
# Register your models here.

class ChatAdmin(admin.ModelAdmin):
    list_display = ['classroom_id', 'student_email']

admin.site.register(Chat)
