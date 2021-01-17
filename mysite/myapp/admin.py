from django.contrib import admin
from myapp.models import Account, FileMod, Logs
from django.contrib.auth.admin import UserAdmin

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login', 'is_superuser' )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class FileAdmin(admin.ModelAdmin):
   readonly_fields = ('upload_date', "is_public")

class LogsAdmin(admin.ModelAdmin):
   readonly_fields = ('userS', 'action', 'action_date')

admin.site.register(Account, AccountAdmin)
admin.site.register(FileMod, FileAdmin)
admin.site.register(Logs, LogsAdmin)
