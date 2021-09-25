from django.contrib import admin

from insurance.models import Policy, Quote, PolicyLog


class PolicyAdmin(admin.ModelAdmin):
    model = Policy
    list_display = ('type', 'premium', 'cover')
    fields = ('type', 'premium', 'cover')


class QuoteAdmin(admin.ModelAdmin):
    model = Quote
    list_display = ('policy', 'customer', 'state')
    fields = ('policy', 'customer', 'state')


class PolicyLogAdmin(admin.ModelAdmin):
    model = PolicyLog
    list_display = ('quote', 'log', 'created_at')
    fields = ('quote', 'log', 'created_at')


admin.site.register(Policy, PolicyAdmin)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(PolicyLog, PolicyLogAdmin)

