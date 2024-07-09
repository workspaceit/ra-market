from django.contrib import admin
from ra_marketplace.models import Pricing, UserPaymentHistory, Campaigns, LocationAdjustment, RehabCalculatorFields
from django.contrib.auth.models import Group, User


class MyAdminSite(admin.AdminSite):
    site_header = 'Housevise Admin Panel'
    site_title = 'Housevise Admin Panel'
    index_title = 'Housevise Admin'


class AdminUserPaymentHistory(admin.ModelAdmin):
    list_display = ('user', 'type', 'amount', 'payment_for', 'created_at',)
    list_filter = ('user', 'payment_for', 'type', 'created_at',)
    search_fields = ('amount', 'payment_for', 'created_at',)
    list_per_page = 20
    list_max_show_all = 50
    actions_on_top = False
    actions_on_bottom = True

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AdminCampaign(admin.ModelAdmin):
    list_display = ('name', 'status', 'budget', 'cost', 'direct_mail_status', 'created_at',)
    list_filter = ('status', 'direct_mail_status',)
    search_fields = ('name', 'budget', 'cost', 'status', 'direct_mail_status',)
    actions_on_top = False
    actions_on_bottom = True
    list_editable = ('budget', 'status', 'direct_mail_status',)
    list_per_page = 10
    list_max_show_all = 20

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AdminUser(admin.ModelAdmin):
    fields = ['username', 'email', 'groups', 'user_permissions', 'is_active', 'is_superuser']
    readonly_fields = ['username', 'email', 'groups']
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'last_login')
    list_filter = ('username', 'email',)
    search_fields = ('username', 'email',)
    actions_on_top = False
    actions_on_bottom = True
    list_per_page = 10
    list_max_show_all = 20

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AdminGroup(admin.ModelAdmin):
    fields = ['name', 'permissions']
    readonly_fields = ['name']
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    actions_on_top = False
    actions_on_bottom = True
    list_per_page = 10
    list_max_show_all = 20

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AdminLocationAdjustment(admin.ModelAdmin):
    fields = ['state', 'project_management_cost', 'location_adjustment_cost']
    # readonly_fields = ['state']
    list_display = ('state', 'project_management_cost', 'location_adjustment_cost')
    list_filter = ('state',)
    list_editable = ('project_management_cost', 'location_adjustment_cost')
    search_fields = ('state',)
    actions_on_top = False
    actions_on_bottom = True
    list_per_page = 10
    list_max_show_all = 20

    # def has_add_permission(self, request):
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False


class AdminRehabCalculatorFields(admin.ModelAdmin):
    fields = ['parameter', 'rehabType', 'touchUpCost', 'repairCost', 'replaceCost', 'average', 'good', 'high']
    readonly_fields = ['good']
    list_display = ('parameter', 'rehabType', 'touchUpCost', 'repairCost', 'replaceCost', 'average', 'good', 'high')
    list_filter = ('rehabType',)
    list_editable = ('touchUpCost', 'repairCost', 'replaceCost', 'average', 'high')
    search_fields = ('rehabType', 'parameter',)
    actions_on_top = False
    actions_on_bottom = True
    list_per_page = 30
    list_max_show_all = 30

    # def has_add_permission(self, request):
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False


class AdminPricing(admin.ModelAdmin):
    fields = ['membership_id', 'plan_name', 'area', 'free_inbound_limit', 'free_outbound_limit', 'unit', 'inbound_unit_price', 'outbound_unit_price']
    list_display = ('membership_id', 'plan_name', 'area', 'free_inbound_limit', 'free_outbound_limit', 'unit', 'inbound_unit_price', 'outbound_unit_price')
    list_filter = ('membership_id', 'plan_name', 'area',)
    list_editable = ('area', 'free_inbound_limit', 'free_outbound_limit', 'unit', 'inbound_unit_price', 'outbound_unit_price')
    search_fields = ('membership_id', 'plan_name', 'area',)
    actions_on_top = False
    actions_on_bottom = True
    list_per_page = 30
    list_max_show_all = 30

    # def has_add_permission(self, request):
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False


admin_site = MyAdminSite()
admin_site.register(UserPaymentHistory, AdminUserPaymentHistory)
admin_site.register(Campaigns, AdminCampaign)
admin_site.register(Group, AdminGroup)
admin_site.register(User, AdminUser)
admin_site.register(LocationAdjustment, AdminLocationAdjustment)
admin_site.register(RehabCalculatorFields, AdminRehabCalculatorFields)
admin_site.register(Pricing, AdminPricing)
