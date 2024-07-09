from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.decorators import api_view

from ra_marketplace.logger import log
from ra_marketplace.models import Campaigns, Leads, LeadStatus, TwilioInboundCall, TwilioInboundSms, \
    TwilioOutboundSms, SendgridInboundEmails, SendgridOutboundEmails
from ra_marketplace.util.team_info import get_parent, get_team_members_array
from celery_app.tasks import update_sms_view_status


def create_default(user):
    campaign = Campaigns.objects.create(user=user, name='Default campaign', type_id=8, target_id=4)

    Leads.objects.create(
        first_name='Jane',
        lead_type='Seller',
        phone_number='8665430987',
        email_address='sample_email@gmail.com',
        property_address='123 Main St, Edison, NJ 08817, USA',
        mailing_address='123 Main St, Edison, NJ 08817, USA',
        notes='<figure class="media"><oembed url="https://www.youtube.com/watch?v=y2X7c9TUQJ8"></oembed></figure>',
        campaign=campaign,
        lead_source=None,
        dnc='N',
        reverse_priority='0',
        lead_status=LeadStatus.objects.filter(Q(status_code='new') & Q(user=get_parent(user))).first(),
        city='Edison',
        last_name='Doe',
        state='NJ',
        street_address='123 Main St',
        zip='8817',
        came_by='manual',
        escrow='0',
        asking_price='150000',
        bath='2',
        bed='3',
        lot_sq_footage='10000',
        sq_footage='1850',
        year_built='2018',
    )
    print('Default campaign Campaign created.')


def get_users_list(user):
    team_members_id = get_team_members_array(user)
    member_list = []
    for user_id in team_members_id:
        member_list.append(get_user_model().objects.filter(id=user_id).first())

    return member_list


@api_view(['GET'])
def get_call_logs(request):
    user = request.user

    default = Campaigns.objects.filter(user=user, name='Default campaign')
    if len(default) <= 0:
        create_default(user)

    campaigns = Campaigns.objects.filter(user__in=get_users_list(user)).order_by('-created_at')

    phone_list = []
    for campaign in campaigns:
        if campaign.user_phone:
            phone_list.append(campaign.user_phone.phone_number)

    logs = []

    calls = TwilioInboundCall.objects.filter(Q(From__in=phone_list) | Q(To__in=phone_list)) \
        .exclude(CallStatus='in-progress').exclude(CallStatus=None) \
        .values('id', 'To', 'From', 'CallStatus', 'created_at', 'lead', 'seen', 'Direction', 'RecordingUrl')

    for call in calls:
        lead = Leads.objects.filter(id=call['lead']).first()
        inbound = {
            'property_address': lead.property_address.strip() if lead and (
                        lead.property_address and lead.property_address.strip() != '') else None,
            'lead_name': lead.first_name.strip() if lead and (
                        lead.first_name and lead.first_name.strip() != '') else None,
            'called_from': call['From'],
            'called_to': call['To'],
            'direction': call['Direction'],
            'time': call['created_at'],
            'status': call['CallStatus'],
            'data': call['RecordingUrl']
        }

        logs.append(inbound)

    queryset = sorted(logs, key=lambda i: i['time'], reverse=True)

    return JsonResponse(queryset, safe=False)


@api_view(['GET'])
def get_sms_logs(request):
    default = Campaigns.objects.filter(user=request.user, name='Default campaign')
    if len(default) <= 0:
        create_default(request.user)

    campaigns = Campaigns.objects.filter(user__in=get_users_list(request.user)).order_by('-created_at')

    phone_list = []
    for campaign in campaigns:
        if campaign.user_phone:
            phone_list.append(campaign.user_phone.phone_number)

    logs = []

    inbound_sms_qs = reversed(TwilioInboundSms.objects.filter(To__in=phone_list).values('To', 'From').distinct())

    outbound_sms_qs = reversed(TwilioOutboundSms.objects.filter(send_from__in=phone_list, initiated=True)
                               .values('to', 'send_from').distinct())

    for sms in inbound_sms_qs:
        msg = TwilioInboundSms.objects.filter(Q(To=sms['To']) & Q(From=sms['From'])).last()
        unseen_count = TwilioInboundSms.objects.filter(Q(To=sms['To']) & Q(From=sms['From']) & Q(seen=False)).count()
        outbound_msg = TwilioOutboundSms.objects.filter(Q(send_from=sms['To']) & Q(to=sms['From'])).last()
        entry = {
            'property_address': msg.lead.property_address.strip() if msg.lead and (
                    msg.lead.property_address and msg.lead.property_address.strip() != '') else None,
            'lead_name': msg.lead.first_name.strip() if msg.lead and (
                    msg.lead.first_name and msg.lead.first_name.strip() != '') else None,
            'sent_from': sms['From'],
            'sent_to': sms['To'],
            'message': outbound_msg.message.text if outbound_msg and msg.created_at < outbound_msg.created_at else msg.Body,
            'unseen_count': unseen_count,
            'direction': 'inbound',
            'time': msg.created_at,
        }

        logs.append(entry)

    for sms in outbound_sms_qs:
        msg = TwilioOutboundSms.objects.filter(Q(send_from=sms['send_from']) & Q(to=sms['to'])).last()
        logs.append({
            'property_address': None,
            'lead_name': None,
            'unseen_count': 0,
            'sent_from': sms['send_from'],
            'sent_to': sms['to'],
            'message': msg.message.text,
            'direction': 'outbound',
            'time': sms['time'],
        })

    queryset = sorted(logs, key=lambda i: i['time'], reverse=True)

    return JsonResponse(queryset, safe=False)


@api_view(['GET'])
def get_sms_details(request):
    number_own = '+' + request.GET['my_number'].strip() if 'my_number' in request.GET else None
    number_from = '+' + request.GET['from_number'].strip() if 'from_number' in request.GET else None

    if not number_own or not number_from:
        return JsonResponse({'message': 'Need Both number_own and number from to proceed'}, safe=False, status=500)

    logs = []

    inbound_sms_qs = TwilioInboundSms.objects.filter(To=number_own, From=number_from) \
        .order_by('id')

    outbound_sms_qs = TwilioOutboundSms.objects.filter(to=number_from, send_from=number_own) \
        .order_by('id')

    response = {}
    for sms in inbound_sms_qs:
        if 'lead' not in response and sms.lead:
            response['lead'] = sms.lead.id
            response['campaign'] = sms.lead.campaign.id
        logs.append({
            'message': sms.Body,
            'direction': 'inbound',
            'time': sms.created_at,
        })

    for sms in outbound_sms_qs:
        logs.append({
            'message': sms.message.text,
            'direction': 'outbound',
            'time': sms.created_at,
        })

    if 'lead' not in response:
        response['lead'] = None
        response['campaign'] = None

    queryset = sorted(logs, key=lambda i: i['time'], reverse=False)
    response['messages'] = queryset

    try:
        update_sms_view_status.delay(number_own, number_from)
    except:
        log.error('Failed To Update Seen Values')

    return JsonResponse(response, safe=False)


@api_view(['GET'])
def get_email_logs(request):
    user = request.user

    service = request.META.get('HTTP_REFERER').split('/')[2]

    print(service)

    default = Campaigns.objects.filter(user=user, name='Default campaign')
    if len(default) <= 0:
        create_default(user)

    campaigns = Campaigns.objects.filter(user__in=get_users_list(user)).order_by('-created_at')

    email_list = []
    for campaign in campaigns:
        email_list.append(campaign.uid + "@" + service)

    logs = []

    inbound_email_qs = reversed(SendgridInboundEmails.objects.filter(to__in=email_list)
                                .values('to', 'From').distinct())

    outbound_email_qs = reversed(SendgridOutboundEmails.objects.filter(send_from__in=email_list, initiated=True)
                                 .values('to', 'send_from').distinct())

    for email in inbound_email_qs:
        email_details = SendgridInboundEmails.objects.filter(Q(to=email['to']) & Q(From=email['From'])).last()
        email_outbound = SendgridOutboundEmails.objects.filter(
            Q(to=email['From']) & Q(send_from=email['to'])).last()
        logs.append({
            'subject': email_details.subject,
            'sent_from': email_details.From,
            'sent_to': email_details.to,
            'message': email_outbound.message.text if email_outbound and email_details.created_at < email_outbound.created_at else email_details.text,
            'direction': 'inbound',
            'time': email_details.created_at,
        })

    for email in outbound_email_qs:
        email_details = SendgridOutboundEmails.objects.filter(
            Q(to=email['to']) & Q(send_from=email['send_from'])).last()
        logs.append({
            'subject': email_details.message.subject,
            'sent_from': email_details.send_from,
            'sent_to': email_details.to,
            'message': email_details.message.text,
            'direction': 'outbound',
            'time': email_details.created_at,
        })

    queryset = sorted(logs, key=lambda i: i['time'], reverse=True)

    return JsonResponse(queryset, safe=False)


@api_view(['GET'])
def get_email_details(request):
    email_own = request.GET['my_email'].strip() if 'my_email' in request.GET else None
    email_from = request.GET['from_email'].strip() if 'from_email' in request.GET else None

    if not email_own or not email_from:
        return JsonResponse({'message': 'Need Both my_email and from_email to proceed'}, safe=False, status=500)

    logs = []

    inbound_email_qs = SendgridInboundEmails.objects.filter(to=email_own, From=email_from) \
        .order_by('id')

    outbound_email_qs = SendgridOutboundEmails.objects.filter(to=email_from, send_from=email_own) \
        .order_by('id')

    response = {}
    for email in inbound_email_qs:
        if 'lead' not in response and email.lead:
            response['lead'] = email.lead.id
            response['campaign'] = email.lead.campaign.id
        logs.append({
            'sent_from': email.From,
            'message': email.html,
            'subject': email.subject,
            'direction': 'inbound',
            'time': email.created_at,
        })

    for email in outbound_email_qs:
        logs.append({
            'sent_from': email.send_from,
            'message': email.message.html,
            'subject': email.message.subject,
            'direction': 'outbound',
            'time': email.created_at,
        })

    if 'lead' not in response:
        response['lead'] = None
        response['campaign'] = None

    queryset = sorted(logs, key=lambda i: i['time'], reverse=False)
    response['messages'] = queryset

    return JsonResponse(response, safe=False)
