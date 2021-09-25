from django_filters import rest_framework as d_filters
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from insurance.api import serializers, filtersets
from insurance.api.serializers import PolicyLogHistorySerializer, PolicyLogSerializer
from insurance.models import Quote


class QuoteViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Quote.objects.all()
    serializer_class = serializers.QuoteCreateSerializer
    action_serializers = {
        'create': serializers.QuoteCreateSerializer,
        'update': serializers.QuoteUpdateSerializer
    }
    action_permission_classes = {
        'create': (permissions.IsAuthenticated,),
        'update': (permissions.IsAdminUser,),
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)
        return super().get_serializer_class()

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.action_permission_classes[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return super().get_permissions()


class PolicyViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Quote.objects.all()
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = serializers.CustomerPolicySerializer
    filter_backends = (d_filters.DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = filtersets.PolicyFilter

    @action(methods=('get',), detail=True, permission_classes=(permissions.IsAdminUser,),
            url_path='history', url_name='fetch_history')
    def fetch_history(self, request, pk=None):
        quote = get_object_or_404(Quote, id=pk)
        log_qs = quote.logs.all().order_by('-created_at')
        return Response(PolicyLogSerializer(log_qs, many=True).data)

