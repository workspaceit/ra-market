from rest_framework import viewsets, views, generics, status
from rest_framework.decorators import api_view, action, parser_classes
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import json

from ra_marketplace.models import PropertyPhotos
from ra_marketplace.serializers import PropertyPhotosSerializer


class PropertyPhotosViewSet(viewsets.ModelViewSet):
    queryset = PropertyPhotos.objects.all()
    serializer_class = PropertyPhotosSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = PropertyPhotos.objects.all()
        property_info_id = self.request.query_params.get('property_info_id', None)
        if property_info_id is not None:
            queryset = queryset.filter(property_info_id=property_info_id)
        return queryset

    @action(detail=False, url_path='clear-room-photos', methods=['post'])
    def clear_room_photos(self, request):
        body = json.loads(request.body)
        if 'property_id' not in body:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        property_id = body['property_id']
        property_photos = PropertyPhotos.objects.filter(property_info_id=property_id)
        for property_photo in property_photos:
            property_photo.room.clear()
        return Response({}, status=status.HTTP_200_OK)

    @action(detail=False, url_path='get-by-room', methods=['get'])
    def get_by_room(self, request):
        position = self.request.query_params.get('room_type', None)
        room_id = self.request.query_params.get('room_id', None)
        property_info_id = self.request.query_params.get('property_info_id', None)

        if not property_info_id:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        property_photos = None
        if position:
            property_photos = PropertyPhotos.objects.filter(room__room_type_id=position,
                                                            property_info_id=property_info_id).distinct()
        elif room_id:
            property_photos = PropertyPhotos.objects.filter(room__id=room_id,
                                                            property_info_id=property_info_id).distinct()

        return Response(self.serializer_class(property_photos, many=True).data, status=status.HTTP_200_OK)

    @action(detail=False, url_path='delete-room', methods=['DELETE'])
    def delete_photo_room(self, request):
        photo_id = request.GET['photo_id']
        room_id = request.GET['room_id']
        PropertyPhotos.room.through.objects.filter(propertyphotos_id=photo_id, room_id=room_id).delete()
        return Response('Deleted photo_id {} room_id {}'.format(photo_id, room_id))
