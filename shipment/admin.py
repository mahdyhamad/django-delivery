from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea
from .models import Shipment, Package
# Register your models here.


@admin.register(Package)
class PackageInline(admin.ModelAdmin):
    list_display = ['shipment', 'size', 'weight']

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Package.objects.all()
        else:
            return Package.objects.filter(client__exact=request.user.userprofile.client)


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['client', 'drop_off_user', 'pickup_user', 'price', 'paid', 'status']
    search_fields = ('drop_off_user__full_name', 'pickup_user__full_name')
    fields = ['drop_off_user', 'pickup_user', 'credentials', 'package', 'price', 'paid']
    readonly_fields = ['id', 'client']
    list_filter = ['paid', 'status']

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Shipment.objects.all()
        else:
            return Shipment.objects.filter(client__exact=request.user.userprofile.client)

    def get_fields(self, request, obj=None):
        fields = super(ShipmentAdmin, self).get_fields(request, obj)
        if request.user.is_superuser:
            fields += ('client',)
        return fields