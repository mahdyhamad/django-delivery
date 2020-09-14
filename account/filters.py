from django_filters import FilterSet, BooleanFilter
from account.models import User


class UserFilter(FilterSet):
    exclude_store = BooleanFilter(method="exclude_store_filter")

    class Meta:
        model = User
        fields = {
            'first_name': ['icontains'],
            'email': ['icontains'],
            'username': ['icontains']
        }

    def exclude_store_filter(self, queryset, name, value):
        if value:
            return queryset.exclude(is_shop=True)

