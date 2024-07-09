import re

from django.core.exceptions import FieldDoesNotExist
from django.http import JsonResponse
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from ra_marketplace.models import LeadWebForms, Leads, LeadCustomFieldKeys
from ra_marketplace.serializers import LeadWebFormsSerializer


class ActionBasedPermission(AllowAny):
    """
    Grant or deny access to a view, based on a mapping in view.action_permissions
    """

    def has_permission(self, request, view):
        print(view.action)
        for klass, actions in getattr(view, 'action_permissions', {}).items():
            if view.action in actions:
                return klass().has_permission(request, view)
        return False


class LeadWebFormsViewSet(viewsets.ModelViewSet):
    queryset = LeadWebForms.objects.all()
    serializer_class = LeadWebFormsSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering = ['-id']

    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAuthenticated: ['update', 'partial_update', 'destroy', 'list', 'create', 'get_leads_fields'],
        AllowAny: ['retrieve']
    }

    def get_queryset(self):
        queryset = LeadWebForms.objects.filter(user=self.request.user)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = LeadWebForms.objects.get(id=kwargs['pk'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request.data['user'] = self.request.user.id
        print(request.__dict__)
        return super().create(request, *args, **kwargs)

    @action(methods=['GET'], detail=False, url_path='get-leads-fields')
    def get_leads_fields(self, request):
        try:
            return_data = {'system_fields': [], 'custom_fields': []}

            description = ['notes', 'offer_description']
            dropdown = ['lead_type', 'dnc', 'escrow', 'occupancy']
            dropdown_options = {
                'lead_type': [
                    {'key': ' ', 'value': ' '},
                    {'key': 'Seller', 'value': 'Seller'},
                    {'key': 'Buyer', 'value': 'Buyer'},
                    {'key': 'Potential Lender', 'value': 'Potential Lender'}
                ],
                'dnc': [
                    {'key': 'Yes', 'value': 'Y'},
                    {'key': 'No', 'value': 'N'},
                ],
                'escrow': [
                    {'key': 'Yes', 'value': 1},
                    {'key': 'No', 'value': 0},
                ],
                'occupancy': [
                    {'key': ' ', 'value': ' '},
                    {'key': 'Vacant', 'value': 'Vacant'},
                    {'key': 'Owner Occupied', 'value': 'Owner Occupied'},
                    {'key': 'Tenants', 'value': 'Tenants'}
                ],
            }

            field_list = [f.get_attname() for f in Leads._meta.fields]
            unwanted_num = ['id', 'reverse_priority', 'came_by', 'inbound_id', 'offer_dt', 'lead_source_id',
                            'created_at', 'updated_at', 'lead_list_details_id', 'contact_id', 'is_verified']

            fields = [ele for ele in field_list if ele not in unwanted_num]

            index = 0
            for field in fields:
                field_view_name = re.sub('[^a-zA-Z0-9 \n\.]', ' ', field).replace('id', '').capitalize()

                not_editable = False
                field_type = 'text'
                field_options = None
                is_selected = True

                if index > 10:
                    is_selected = False

                if field in ['lead_status_id', 'campaign_id']:
                    not_editable = True
                    is_selected = True

                if field in description:
                    field_type = 'description'
                elif field in dropdown:
                    field_type = 'dropdown'
                    field_options = dropdown_options[field]

                obj = {
                    'field_name': field_view_name,
                    'field_code': field,
                    'is_selected': is_selected,
                    'is_disabled': not_editable,
                    'is_id_selectable': not_editable,
                    'associate_id': None,
                    'associate_data': None,
                    'field_type': field_type,
                    'field_options': field_options,
                }
                return_data['system_fields'].append(obj)
                index = index + 1

            custom_fields = LeadCustomFieldKeys.objects.filter(user=request.user)

            for field in custom_fields:
                obj = {
                    'field_name': field.name,
                    'field_code': field.name.lower().strip().replace(' ', '_'),
                    'is_selected': False,
                    'is_disabled': False,
                    'is_id_selectable': False,
                    'associate_id': field.id,
                    'associate_data': None,
                    'field_type': 'text',
                    'field_options': None,
                }
                return_data['custom_fields'].append(obj)

            return JsonResponse(status=200, data=return_data, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse(status=500, data={'error': 'Something Went Wrong'}, safe=False)
