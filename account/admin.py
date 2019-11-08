from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

class AccountAdmin(UserAdmin):
    list_display        = ('username', 'email', 'is_admin', 'last_login', 'date_joined')
    search_fields       = ('username', 'email', 'last_login', 'is_admin')
    readonly_fields     = ('date_joined', 'last_login', 'dob')

    filter_horizontal   = ()
    list_filter         = ()
    fieldsets           = ()

admin.site.register(Account, AccountAdmin)
