from django.contrib import admin

from customer.models import Customer


class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display = ('user', 'dob')
    fields = ('user', 'dob')


admin.site.register(Customer, CustomerAdmin)

