from django.urls import path
from rest_framework import routers

from .views import (
    ExchangeRatesViewSet,
    UpdateRatesAPIView,
)


router = routers.SimpleRouter()
router.register(r'rates', ExchangeRatesViewSet)

app_name = 'api'
urlpatterns = [
    path('updateRates/', UpdateRatesAPIView.as_view(), name='update-rates'),
] + router.urls
