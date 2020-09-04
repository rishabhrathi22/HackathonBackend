from django.contrib import admin
from .models import Institute

class InstituteAdmin(admin.ModelAdmin):
	list_display = ['institution_name', 'email', 'contact_person', 'phone_number', 'status']
	search_fields = ('institution_name',)
	ordering = ('institution_name',)  

admin.site.register(Institute, InstituteAdmin)