from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.conf import settings

@api_view(['POST'])
def send_with_mail(request):

    # sender = request.POST.get('sender')
    receiver = request.POST.get('receiver')
    subject = request.POST.get('subject')
    mail_body = request.POST.get('body')

    send_mail(subject=subject,
              message=mail_body,
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[receiver],
              fail_silently=False
              )

    return Response(subject)
