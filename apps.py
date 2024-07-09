from django.contrib.admin.apps import AdminConfig
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


#
# class TwilioInboundConfig(AppConfig):
#     name = 'ra_marketplace'
#     verbose_name = _('TwilioInbound')
#
#     def ready(self):
#         import ra_marketplace.signals_old


class MyAdminConfig(AdminConfig):
    default_site = 'ra_marketplace.admin.MyAdminSite'


class PaymentConfig(AppConfig):
    name = 'ra_marketplace'
    verbose_name = _('HouseVize Settings')

    def ready(self):
        print("loading signals")
        import ra_marketplace.signals
