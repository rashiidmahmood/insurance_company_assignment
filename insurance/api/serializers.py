from rest_framework import serializers

from customer.api.serializers import CustomerSerializer
from insurance.models import Quote, Policy, PolicyLog


class QuoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ('policy', 'customer')

    def validate_customer(self, customer):
        if all((
                not self.context['request'].user.is_staff,
                not self.context['request'].user == customer.user
        )):
            raise serializers.ValidationError("Invalid customer!")
        return customer

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.create_log(log=f"Quote created by customer '{self.context['request'].user.email}'")
        return instance


class QuoteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ('state',)

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.create_log(
            log=f"Status changed to '{instance.state}' by '{self.context['request'].user.email}'"
        )
        return instance


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ('type', 'premium', 'cover')


class CustomerPolicySerializer(serializers.ModelSerializer):
    policy = PolicySerializer()
    customer = CustomerSerializer()

    class Meta:
        model = Quote
        fields = ('policy', 'customer', 'state')


class PolicyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyLog
        fields = ('log', 'created_at')


class PolicyLogHistorySerializer(serializers.ModelSerializer):
    policy = PolicySerializer()
    logs = PolicyLogSerializer(many=True)

    class Meta:
        model = Quote
        fields = ('policy', 'logs')