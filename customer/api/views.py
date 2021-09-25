from rest_framework import mixins, permissions, viewsets

from customer.api import serializers
from customer.models import Customer


class CustomerCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Customer.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.CustomerCreateSerializer
