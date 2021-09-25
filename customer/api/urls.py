from django.urls import path, include
from rest_framework import routers

from customer.api import views

app_name = "customer_api"

router = routers.DefaultRouter()
router.register(r"v1/create_customer", views.CustomerCreateViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
