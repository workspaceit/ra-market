import requests
from rest_framework import status
from ra_marketplace.settings import BANKRUPTCY_SEARCH_API_URL
from rest_framework.response import Response
from rest_framework.views import APIView


class LeadSearchBankruptcyViewSet(APIView):
    def get(self, request):
        auth_token = '8opsz1juf71jwi3ohppgsr2lz'
        hed = {'Authorization': 'Bearer ' + auth_token}
        path = request.get_full_path()
        key = 'lead-search/bankruptcy?'
        url = BANKRUPTCY_SEARCH_API_URL + '?' + path[path.index(key) + len(key):]
        res = requests.get(url, headers=hed).json()
        return Response(res, status=status.HTTP_200_OK)