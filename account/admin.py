from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import UserProfile, User


class UserProfileAdmin(admin.TabularInline):
    model = UserProfile

    def get_min_num(self, request, obj=None, **kwargs):
        return 1

    def get_max_num(self, request, obj=None, **kwargs):
        return 1


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileAdmin, ]
    list_display = UserAdmin.list_display + ('full_name',)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)