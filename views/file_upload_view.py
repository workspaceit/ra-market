import os
import re
import time
import traceback

import boto3
import requests
from rest_framework.decorators import parser_classes, api_view
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status

from ra_marketplace import settings
from ra_marketplace.models import PropertyPhotos
from ra_marketplace.serializers import PropertyPhotosSerializer
from ra_marketplace.util.file_upload import file_upload


@api_view(['POST'])
@parser_classes((MultiPartParser,))
def upload_property_photos(request):
    s3_bucket = get_s3_bucket()
    if 'file' not in request.FILES and 'file_url' not in request.data:
        return Response({'message': 'Please Include a file to be uploaded!'}, status=400)
    if 'property_info_id' not in request.data:
        return Response({'message': 'Please Include a Property Info Id!'}, status=400)

    file = None
    if 'file' not in request.FILES:
        url = request.data['file_url']
        file = download_file(url)
        if not file:
            return Response({'message': 'Please Include a file to be uploaded!'}, status=400)
    else:
        file = request.FILES['file']

    property_info_id = request.data['property_info_id']
    file_path = "property_photos/{}/{}".format(property_info_id, file.name.split('/')[-1])
    s3_url = "https://s3.{}.amazonaws.com/{}/{}".format(settings.AWS_S3_REGION_NAME, settings.S3_BUCKET_NAME, file_path)

    response = None
    if 'file' not in request.FILES:
        # response = s3_bucket.Object(settings.S3_BUCKET_NAME, file_path).upload(file.name)
        response = s3_bucket.meta.client.upload_sms_media_file(file.name, settings.S3_BUCKET_NAME, file_path, ExtraArgs={'ACL': "public-read"})
        os.remove(file.name)
        property_photos = PropertyPhotos(property_info_id=property_info_id, photo_url=s3_url)
        property_photos.save()

        serializer = PropertyPhotosSerializer(property_photos)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    else:
        response = s3_bucket.Object(settings.S3_BUCKET_NAME, file_path).put(Body=file, ACL='public-read')
        if 'ResponseMetadata' in response and 'HTTPStatusCode' in response['ResponseMetadata'] and \
                response['ResponseMetadata']['HTTPStatusCode'] == 200:
            property_photos = PropertyPhotos(property_info_id=property_info_id, photo_url=s3_url)
            property_photos.save()

            serializer = PropertyPhotosSerializer(property_photos)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@parser_classes((MultiPartParser,))
def upload_sms_media_file(request):
    if 'file' not in request.FILES:
        return Response({'message': 'Please Include a file to be uploaded!'}, status=400)
    file = request.FILES['file']
    file_path = "campaign/sms/media/{}/{}".format(str(request.user.id),
                                                  str(time.time()) + '.' + file.name.split('.')[-1])
    try:
        uploaded = file_upload(file, file_path, content_type=file.content_type)
        print(uploaded)
        return Response(uploaded, status=status.HTTP_201_CREATED)
    except:
        traceback.print_exc()
        res = {'status': False, 'msg': 'Failed to upload'}
    return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def download_file(url):
    response = requests.get(url)
    fname = ''
    if "Content-Disposition" in response.headers.keys():
        fname = re.findall("filename=(.+)", response.headers["Content-Disposition"])[0]
        fname = fname.split(";")[0]
        fname = fname.replace('"', '')
    else:
        fname = url.split("/")[-1]

    fname = '/tmp/' + fname
    myfile = open(fname, 'wb')
    myfile.write(response.content)
    # myfile.close()
    return myfile


def get_s3_bucket():
    s3_connection = boto3.resource('s3',
                                   region_name=settings.AWS_S3_REGION_NAME,
                                   aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
                                   aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY)
    return s3_connection
