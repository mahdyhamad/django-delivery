from django.contrib import admin

from account.models import User
from client.models import Client
from shipment.models import Shipment


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ['id', 'name', 'city', 'detailed_address', 'shipments_count', 'total_money_earned']
    readonly_fields = ['id', ]

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Client.objects.all()
        else:
            return Client.objects.filter(id__exact=request.user.userprofile.client.id)

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['users'].queryset = User.objects.filter(userprofile__is_shop=True)
        return super(ClientAdmin, self).render_change_form(request, context, *args, **kwargs)

admin.site.site_url = None
admin.site.site_header = "Drop & Pickup Admin Site"
admin.site.site_title = "Drop & Pickup"
admin.site.index_title = "Site adminstartion"