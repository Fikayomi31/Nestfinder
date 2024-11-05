from django.contrib import admin
from .models import User, AgentProfile, TenantProfile

class AgentProfileInline(admin.StackedInline):
    model = AgentProfile
    can_delete = False
    verbose_name_plural = 'Agent Profile'

class TenantProfileInline(admin.StackedInline):
    model = TenantProfile
    can_delete = False
    verbose_name_plural = 'Tenant Profile'

class UserAdmin(admin.ModelAdmin):
    inlines = (AgentProfileInline, TenantProfileInline)

admin.site.register(User, UserAdmin)
admin.site.register(AgentProfile)
admin.site.register(TenantProfile)
