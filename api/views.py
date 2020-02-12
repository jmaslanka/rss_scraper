from rest_framework import status
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import ExchangeRate
from .serializers import ExchangeRateSerializer
from .tasks import update_exchange_rates


class UpdateRatesAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        update_exchange_rates.delay()
        return Response(status=status.HTTP_200_OK)


class ExchangeRatesViewSet(ReadOnlyModelViewSet):
    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []
    lookup_field = 'currency'
