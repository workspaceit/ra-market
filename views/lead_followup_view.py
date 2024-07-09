from rest_framework import viewsets
from ra_marketplace.models import LeadsFollowUp
from ra_marketplace.serializers import LeadsFollowUpSerializer

# LeadsFollowUp Model has a signal name lead_followup_celery_task is signals.py


class LeadFollowupViewSet(viewsets.ModelViewSet):
    queryset = LeadsFollowUp.objects.all()
    serializer_class = LeadsFollowUpSerializer



