from rest_framework import viewsets

from ra_marketplace.models import AuthorizedServiceAddresses
from ra_marketplace.serializers import AuthorizedServiceAddressesSerializer


class AuthorizedServiceAddressesViewSet(viewsets.ModelViewSet):
    queryset = AuthorizedServiceAddresses.objects.all()
    serializer_class = AuthorizedServiceAddressesSerializer