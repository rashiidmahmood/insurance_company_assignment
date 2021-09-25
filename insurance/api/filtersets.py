from django.db.models import Q

from django_filters import rest_framework as filters

from insurance.models import Quote


class PolicyFilter(filters.FilterSet):
    customer_name = filters.CharFilter(method='filter_by_customer_name')
    customer_dob = filters.DateFilter(field_name='customer__dob')
    policy_type = filters.CharFilter(field_name='policy__type')

    class Meta:
        model = Quote
        fields = (
            'customer_id',
        )

    def filter_by_customer_name(self, queryset, field_name, value):
        queryset = queryset.filter(
            Q(customer__user__first_name__icontains=value) |
            Q(customer__user__last_name__icontains=value)
        )
        return queryset
