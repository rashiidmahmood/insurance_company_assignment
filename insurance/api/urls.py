from django.urls import path, include
from rest_framework import routers

from insurance.api import views

app_name = "insurance_api"

router = routers.DefaultRouter()
router.register(r"v1/quote", views.QuoteViewSet, basename='quote')
router.register(r"v1/policies", views.PolicyViewSet, basename='policy')

urlpatterns = [
    path("", include(router.urls)),
]
