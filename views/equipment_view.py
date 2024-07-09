from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from ra_marketplace.models import Equipment
from ra_marketplace.serializers import EquipmentSerializer


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [AllowAny]
