"""ra_marketplace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from fsbo.views import FsboApiView
from google_api.views import get_google_auth_url, gapi_callback, get_calendar_events, create_calendar_event, \
    is_authorize
from live_message.views import NotificationApiView, ActivityApiView
from ra_marketplace.util.swagger import schema_view
from ra_marketplace.views import webhook_view
from ra_marketplace.views.campaign.campaign_recreate_view import CampaignRecreateViewSet
from ra_marketplace.views.campaign.leads.lead_assignees_view import LeadAssigneesViewSet
from ra_marketplace.views.campaign.leads.lead_tags_view import LeadTagsViewSet
from ra_marketplace.views.campaign.leads.leads_tasks_view import LeadTasksViewSet
from ra_marketplace.views.campaign.leads.user_lead_favourite_fields_view import UserLeadFavouriteFieldsViewSet
from ra_marketplace.views.ckeditor_image_upload_view import ckeditor_image_upload
from ra_marketplace.views.communication_center_view import get_call_logs, get_sms_logs, get_sms_details, get_email_logs, \
    get_email_details
from ra_marketplace.views.contacts.contacts_tag_view import ContactsTagViewSet
from ra_marketplace.views.contacts.contacts_view import ContactsViewSet
from ra_marketplace.views.campaign.leads.lead_attachments_view import LeadAttachmentsViewSet
from ra_marketplace.views.campaign.leads.lead_status_view import LeadStatusViewSet
from ra_marketplace.views.custom_permission_view import get_custom_permissions, get_all_custom_permissions, \
    set_custom_permissions, check_user_custom_permission
from ra_marketplace.views.email_templates_view import EmailTemplatesViewSet
from ra_marketplace.views.help_text_view import HelpTextsViewSet
from ra_marketplace.views.houzes_integration import create_token
from ra_marketplace.views.lead_custom_field_keys_view import LeadCustomFieldKeysViewSet
from ra_marketplace.views.lead_custom_fields_data_view import LeadCustomFieldsDataViewSet
from ra_marketplace.views.lead_notes_view import LeadNotesViewSet
from ra_marketplace.views.lead_search_bankruptcy_view import LeadSearchBankruptcyViewSet
from ra_marketplace.views.lead_search_list_count_view import LeadSearchListCountViewSet
from ra_marketplace.views.lead_search_view import LeadSearchApiView
from ra_marketplace.views.lead_web_forms_view import LeadWebFormsViewSet
from ra_marketplace.views.outbound.twilio_outbound_call_view import TwilioOutboundCallViewSet
from ra_marketplace.views.outbound.twilio_outbound_sms_view import TwilioOutboundSmsViewSet
from ra_marketplace.views.payment.user_credit_card_view import UserCreditCardsViewSet
from ra_marketplace.views.powertrace import power_trace_view
from ra_marketplace.views.property_attachment_view import PropertyAttachmentsViewSet
from ra_marketplace.views.quick_audio_replies_view import QuickAudioRepliesViewSet
from ra_marketplace.views.quick_replies_view import QuickRepliesViewSet
from ra_marketplace.views.sequence.sequence_tasks_view import SequenceTasksViewSet
from ra_marketplace.views.sequence.sequence_view import SequenceViewSet
from ra_marketplace.views.tags_view import TagsViewSet
from ra_marketplace.views.task.task_comments_view import TaskCommentsViewSet
from ra_marketplace.views.task.assigned_members_view import AssignedMemberViewSet
from ra_marketplace.views.task.assigned_tag_view import AssignedTagViewSet
from ra_marketplace.views.campaign.campaign_audio_view import CampaignAudioViewSet
from ra_marketplace.views.campaign.campaign_rvm_information_view import CampaignRvmInformationViewSet
from ra_marketplace.views.campaign.campaign_rvm_view import CampaignRvmViewSet
from ra_marketplace.views.campaign.campaigns_view import CampaignViewSet
from ra_marketplace.views.team_invitation_view import TeamInvitationViewSet
from ra_marketplace.views.templates_view import TemplatesViewSet
from ra_marketplace.views.transaction.deal_analyzer.cost_analysis_view import CostAnalysisViewSet
from ra_marketplace.views.mailer_wizard_info_view import MailerWizardInfoViewSet
from ra_marketplace.views.mailer_wizard_view import MailerWizardViewSet
from ra_marketplace.views.offer_generator_view import OfferGeneratorViewSet
from ra_marketplace.views.payment.payment_view import payment, get_current_user_credit, payment_using_payment_profile, \
    check_and_use_credit, webhook_subscription_failed_event, get_pricing
from ra_marketplace.views.transaction.rehab_calculator.rehab_calculator_fields_view import RehabCalculatorFieldsViewSet
from ra_marketplace.views.transaction.rehab_calculator.location_adjustment_view import LocationAdjustmentViewSet
from ra_marketplace.views.transaction.rehab_calculator.property_deal_details_view import PropertyDealDetailsViewSet
from ra_marketplace.views.file_upload_view import upload_property_photos, upload_sms_media_file
from ra_marketplace.views.goals_view import GoalsViewSet
from ra_marketplace.views.lead_list_details_view import LeadListDetailsViewSet
from ra_marketplace.views.lead_list_view import LeadListViewSet, HouzesLeadList, HouzesLeadListDetails, CheckHouzesToken
from ra_marketplace.views.campaign.leads.leads_view import LeadsViewSet
from ra_marketplace.views.transaction.property_deal_view import PropertyDealViewSet
from ra_marketplace.views.property_info_view import PropertyInfoViewSet
from ra_marketplace.views.contact_info_view import ContactInfoViewSet
from ra_marketplace.views.equipment_view import EquipmentViewSet
from ra_marketplace.views.property_photos_view import PropertyPhotosViewSet
from ra_marketplace.views.transaction.deal_analyzer.purchase_criteria_view import PurchaseCriteriaViewSet
from ra_marketplace.views.room_details_view import RoomDetailsViewSet
from ra_marketplace.views.room_view import RoomViewSet
from ra_marketplace.views.room_type_view import RoomTypeViewSet
from ra_marketplace.views.outbound.sendgrid_outbound_emaile_view import SendgridOutboundEmailsViewSet
from ra_marketplace.views.task.sub_task_view import SubTaskViewSet
from ra_marketplace.views.task.task_assign_member_view import TaskAssignMemberViewSet
from ra_marketplace.views.task.task_attachment_view import TaskAttachmentViewSet
from ra_marketplace.views.task.task_tags_view import TaskTagsViewSet
from ra_marketplace.views.task.tasks_view import TasksViewSet
from ra_marketplace.views.team_members_view import TeamMembersViewSet
from ra_marketplace.views.team_view import TeamViewSet
from ra_marketplace.views.user_details_view import UserDetailsViewSet
from ra_marketplace.views.user_domain_view import UserDomainsViewSet
from ra_marketplace.views.user_home_page_view import UserHomePagesViewSet
from ra_marketplace.views.user_info_view import UserInfoViewSet
from ra_marketplace.views.user_phone_packages import UserPhonePackagesViewSet
from ra_marketplace.views.user_preference_view import UserPreferenceViewSet
from ra_marketplace.views.transaction.deal_analyzer.user_settings_cost_calculator_view import UserSettingsCostCalculatorViewSet
from ra_marketplace.views.user_signature_view import UserSignatureViewSet
from ra_marketplace.views.user_socials_view import UserSocialsViewSet
from ra_marketplace.views.email_sending_view import send_with_mail
from ra_marketplace.views.user_invites_view import UserInvitesViewSet
from ra_marketplace.views.user_details_view import get_user_created_date
from ra_marketplace.views.campaign.campaign_targets_view import CampaignTargetsViewSet
from ra_marketplace.views.campaign.campaign_types_view import CampaignTypesViewSet
from ra_marketplace.views.user_phones_view import UserPhonesViewSet
from ra_marketplace.views.sendgrid_inbound_emails import SendgridInboundEmailsViewSet
from ra_marketplace.views.campaign.leads.lead_sources_view import LeadSourcesViewSet
from ra_marketplace.views.twilio_inbound_sms_view import TwilioInboundSmsViewSet
from ra_marketplace.views.twilio_inbound_call_view import TwilioInboundCallViewSet
from ra_marketplace.views.web_form_inbound_lead_view import WebFormInboundLeadViewSet
from ra_marketplace.views.workflow_triggers_view import WorkflowTriggersViewSet
from ra_marketplace.views.workflow_tasks_view import WorkflowTasksViewSet
from ra_marketplace.views.campaign.celery.Celery_tasks_view import CeleryTasksViewSet
from ra_marketplace.views.campaign.campaign_workflows_view import CampaignWorkflowsViewSet
from ra_marketplace.views.campaign.campaign_sms_log_view import CampaignSMSLogViewSet
from ra_marketplace.views.send_sms_view import SendSMSViewSet
from ra_marketplace.views.campaign.campaign_email_view import CampaignEmailViewSet
from ra_marketplace.views.campaign.campaign_leads_view import CampaignLeadsViewSet
from ra_marketplace.views.lead_followup_view import LeadFollowupViewSet
from ra_marketplace.admin import admin_site
from ra_marketplace.views.zestimate_view import Zestimate, ZestimateComps
from ra_marketplace.views.campaign.leads.lead_contacts_viewset import LeadContactsViewSet
from ra_marketplace.views.city_search_view import CitySearch

router = routers.DefaultRouter()
router.register(r'property-info', PropertyInfoViewSet)
router.register(r'property-attachment', PropertyAttachmentsViewSet)
router.register(r'contact-info', ContactInfoViewSet)
router.register(r'equipment', EquipmentViewSet)
router.register(r'room', RoomViewSet)
router.register(r'room-details', RoomDetailsViewSet)
router.register(r'property-photos', PropertyPhotosViewSet)
router.register(r'room-type', RoomTypeViewSet)
router.register(r'lead-list', LeadListViewSet)
router.register(r'lead-list-details', LeadListDetailsViewSet)
router.register(r'lead-follow', LeadFollowupViewSet)
router.register(r'user-details', UserDetailsViewSet)
router.register(r'user-signature', UserSignatureViewSet)
router.register(r'user-social', UserSocialsViewSet)
router.register(r'goals', GoalsViewSet)
router.register(r'user-preference', UserPreferenceViewSet)
router.register(r'leads', LeadsViewSet)
router.register(r'lead-custom-field-keys', LeadCustomFieldKeysViewSet)
router.register(r'lead_custom_fields_data', LeadCustomFieldsDataViewSet)
router.register(r'lead-notes', LeadNotesViewSet)
router.register(r'team-members', TeamMembersViewSet)
router.register(r'team', TeamViewSet)
router.register(r'team-invite', UserInvitesViewSet)
router.register(r'campaign', CampaignViewSet)
router.register(r'campaign-types', CampaignTypesViewSet)
router.register(r'campaign-targets', CampaignTargetsViewSet)
router.register(r'campaign-sms', CampaignSMSLogViewSet)
router.register(r'campaign-email', CampaignEmailViewSet)
router.register(r'campaign-leads', CampaignLeadsViewSet)
router.register(r'user-phones', UserPhonesViewSet)
router.register(r'lead-sources', LeadSourcesViewSet)
router.register(r'sendgrid-inbound-emails', SendgridInboundEmailsViewSet)
router.register(r'twilio-inbound-sms', TwilioInboundSmsViewSet)
router.register(r'twilio-inbound-calls', TwilioInboundCallViewSet)
router.register(r'web-form-inbound-lead', WebFormInboundLeadViewSet)
router.register(r'workflow-triggers', WorkflowTriggersViewSet)
router.register(r'workflow-tasks', WorkflowTasksViewSet)
router.register(r'celery-tasks', CeleryTasksViewSet)
router.register(r'campaign-workflows', CampaignWorkflowsViewSet)
router.register(r'purchase-criteria', PurchaseCriteriaViewSet)
router.register(r'settings', UserSettingsCostCalculatorViewSet)
router.register(r'deal', PropertyDealViewSet)
router.register(r'location-adjustment', LocationAdjustmentViewSet)
router.register(r'deal-details', PropertyDealDetailsViewSet)
router.register(r'save-analysis', CostAnalysisViewSet)
router.register(r'send-sms', SendSMSViewSet)

router.register(r'task', TasksViewSet)
router.register(r'subtask', SubTaskViewSet)
router.register(r'task-comments', TaskCommentsViewSet)
router.register(r'task-attachment', TaskAttachmentViewSet)
router.register(r'assign-member', AssignedMemberViewSet)
router.register(r'assign-tag', AssignedTagViewSet)
router.register(r'task-assign-member', TaskAssignMemberViewSet)
router.register(r'task-tags', TaskTagsViewSet)

router.register(r'offer', OfferGeneratorViewSet)
router.register(r'mailer-wizard', MailerWizardViewSet)
router.register(r'mailer-wizard-info', MailerWizardInfoViewSet)
router.register(r'campaign-audio', CampaignAudioViewSet)
router.register(r'campaign-rvm-information', CampaignRvmInformationViewSet)
router.register(r'campaign-rvm', CampaignRvmViewSet)
router.register(r'user-info', UserInfoViewSet)
router.register(r'lead-status', LeadStatusViewSet)
router.register(r'lead-attachments', LeadAttachmentsViewSet)
router.register(r'lead-assignee', LeadAssigneesViewSet)
router.register(r'tags', TagsViewSet)
router.register(r'lead-tags', LeadTagsViewSet)
router.register(r'lead-tasks', LeadTasksViewSet)

router.register(r'contacts/tag', ContactsTagViewSet)
router.register(r'contacts', ContactsViewSet)
router.register(r'rehab-calculator-fields', RehabCalculatorFieldsViewSet)
router.register(r'sendgrid-outbound-emails', SendgridOutboundEmailsViewSet)
router.register(r'twilio-outbound-sms', TwilioOutboundSmsViewSet)
router.register(r'twilio-outbound-calls', TwilioOutboundCallViewSet)
router.register(r'templates', TemplatesViewSet)
router.register(r'quick-replies', QuickRepliesViewSet)
router.register(r'quick-audio-replies', QuickAudioRepliesViewSet)
router.register(r'user-credit-cards', UserCreditCardsViewSet)
router.register(r'user-home-pages', UserHomePagesViewSet)
router.register(r'help-texts', HelpTextsViewSet)
router.register(r'team-invitation', TeamInvitationViewSet)
router.register(r'user-phone-packages', UserPhonePackagesViewSet)
router.register(r'lead-web-forms', LeadWebFormsViewSet)

router.register(r'sequences', SequenceViewSet)
router.register(r'sequence-tasks', SequenceTasksViewSet)
router.register(r'campaign-recreate', CampaignRecreateViewSet)
router.register(r'user-domains', UserDomainsViewSet)
router.register(r'user-lead-favourite-fields', UserLeadFavouriteFieldsViewSet)
router.register(r'lead-contacts', LeadContactsViewSet)
router.register(r'email-templates', EmailTemplatesViewSet)
router.register(r'lead-search-list-count', LeadSearchListCountViewSet)

urlpatterns = [
    url('', include('django_prometheus.urls')),
    path('admin/', admin_site.urls),
    path('uploads/property-photos', upload_property_photos),
    path('upload/sms-media-file/', upload_sms_media_file),
    path('user/send-mail', send_with_mail),

    path('pricing/', get_pricing),
    path('add-credit/', payment),
    path('add-credit-using-payment-profile/', payment_using_payment_profile),
    path('get-credit/', get_current_user_credit),
    path('use-credit/', check_and_use_credit),
    path('webhook-subscription-failed-event/', webhook_subscription_failed_event),
    path('webhook/', webhook_view.get),
    path('webhook/create-or-update/', webhook_view.create_or_update),
    path('webhook/lead/<slug:url_key>', webhook_view.create_lead),
    path('houzes-integration/', create_token),
    path('get-createdDate', get_user_created_date),
    url(r'^docs/', include_docs_urls(title='Your API',
                                     authentication_classes=[],
                                     permission_classes=[])),
    path(r'oauth2', include('oauth2_provider.urls', namespace='oauth2')),
    path('twilio/', include('twilio_app.urls', namespace='twilio')),
    # path('phoneNumbers/',availablePhoneNumber),
    # path('celery/', include('celery_app.urls')),
    path('push/', include('push_notification_app.urls')),
    # path(r'^oauth2/$', include('oauth2_provider.urls', namespace='oauth2')),
    url(r'^api-docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^api-docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('live-power-trace/', power_trace_view.lead_power_trace_post),
    path('live-power-trace/getAllRequestByLeadId/', power_trace_view.lead_power_trace_get),
    path('power-trace/create/', power_trace_view.create),
    path('power-trace/getAllRequestByUserId/<int:user_id>/', power_trace_view.get_all_request_by_user_id),
    path('power-trace/getResultById/<int:trace_id>/', power_trace_view.get_result_by_id),
    path('power-trace/update/<int:trace_id>/', power_trace_view.update_power_trace_data),
    path('power-trace/package/<int:package_id>/', power_trace_view.get_package_by_id),
    path('power-trace/checkTraceName/<str:trace_name>/', power_trace_view.check_trace_name),
    path('power-trace/get-running-power-trace-count/', power_trace_view.get_running_power_trace_count),
    path('zestimate/<str:property_address>/', Zestimate.as_view()),
    path('zestimate-comps/<str:zpid>/', ZestimateComps.as_view()),
    path('ckeditor-image-upload/', ckeditor_image_upload),

    path('fsbo/list/', FsboApiView.as_view(), name='fsbo-list-api'),
    path('communication/get-call-logs/', get_call_logs),
    path('communication/get-sms-logs/', get_sms_logs),
    path('communication/get-sms-details/', get_sms_details),
    path('communication/get-email-logs/', get_email_logs),
    path('communication/get-email-details/', get_email_details),
    # path('live-message/test/', NotificationApiView.as_view(), name='notification-api'),
    # path('live-message/test/activity/', ActivityApiView.as_view(), name='live_activity_api')

    path('google_api/is_authorize', is_authorize),
    path('google_api/get_auth_url', get_google_auth_url),
    path('google_api/gapi_callback', gapi_callback),
    path('google_api/get_calendar_events', get_calendar_events),
    path('google_api/create_calendar_event', create_calendar_event),

    path('lead-search/city-search', CitySearch.as_view(), name='city_search'),
    path('lead-search/filter/', LeadSearchApiView.as_view()),
    path('lead-search/bankruptcy', LeadSearchBankruptcyViewSet.as_view()),
    path('google_api/create_calendar_event', create_calendar_event),

    path('get-all-custom-permissions/', get_all_custom_permissions),
    path('get-custom-permissions/', get_custom_permissions),
    path('set-custom-permissions/', set_custom_permissions),
    path('check-user-custom-permission/', check_user_custom_permission),
    path('check-houzes-authentication/', CheckHouzesToken.as_view()),
    path('houzes-list-add/<str:token>/', HouzesLeadList.as_view()),
    path('houzes-property-add/<str:token>/', HouzesLeadListDetails.as_view())

]

urlpatterns += router.urls
