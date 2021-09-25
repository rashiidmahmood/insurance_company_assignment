from django.db import models
from model_utils import Choices

from customer.models import Customer


class Policy(models.Model):
    TYPES = Choices('personal-accident',)

    type = models.CharField(choices=TYPES, max_length=50)
    premium = models.PositiveIntegerField()
    cover = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'Policies'

    def __str__(self):
        return f'{self.get_type_display()}'


class Quote(models.Model):
    STATE = Choices('new', 'accepted', 'active')

    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    state = models.CharField(choices=STATE, max_length=20, default=STATE.new)

    def __str__(self):
        return f'{self.policy}-{self.customer}({self.get_state_display()})'

    def create_log(self, log):
        PolicyLog.objects.create(quote=self, log=log)


class PolicyLog(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='logs')
    log = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.log}'
