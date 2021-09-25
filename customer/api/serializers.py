from rest_framework import serializers

from users.models import User
from customer.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Customer
        fields = ('email', 'first_name', 'last_name', 'dob')


class CustomerCreateSerializer(CustomerSerializer):
    def validate_email(self, email):
        email = email.strip().lower()
        if User.objects.filter(email__iexact=email.strip()).exists():
            raise serializers.ValidationError('Email already exists!')
        return email

    def create(self, validated_data):
        user = User.objects.create(**validated_data.pop('user'))
        user.set_password('customer@123$')
        customer = Customer.objects.create(user=user, dob=validated_data['dob'])
        return customer

