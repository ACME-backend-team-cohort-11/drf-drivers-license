from django.contrib import admin
from .models import NationalId

@admin.register(NationalId)
class NationalIdAdmin(admin.ModelAdmin):
    list_display = ('idNo', 'firstName', 'middleName', 'lastName', 'DOB', 'Sex', 'Passport', 'issuedAt')
    search_fields = ('idNo', 'firstName', 'middleName', 'lastName')
