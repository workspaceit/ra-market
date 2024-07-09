from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter

from ra_marketplace.models import QuickReplies
from ra_marketplace.serializers import QuickRepliesSerializer


class QuickRepliesViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['type']
    search_fields = ['type']
    ordering = ['id']
    queryset = QuickReplies.objects.all()
    serializer_class = QuickRepliesSerializer

    def get_queryset(self):
        return QuickReplies.objects.filter(Q(user_id=None) | Q(user_id=self.request.user.id))
