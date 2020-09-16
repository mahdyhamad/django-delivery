from django.contrib import admin

# Register your models here.
from credentials.models import Credentials

@admin.register(Credentials)
class CredentialsAdmin(admin.ModelAdmin):
    readonly_fields = ['pickup_cred', 'drop_off_cred']