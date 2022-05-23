from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
from .models import Profile

from django.utils.html import format_html
# Register your models here.


class AccountAdmin(UserAdmin):
    model = Account
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'last_login', 'is_active')
    ordering = ('email',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_active')}
        ),
    )

class ProfileAdmin(admin.ModelAdmin):
    def picture(self, object):
        return format_html('<img src="{}"style="border-radius:50%"; hight="30"; width="30";>'.format(object.profile_picture.url))
        
    picture.short_description = "Profile Picture"
    picture.allow_tags = True

    list_display = ('picture', 'user','city', 'state', 'country')

admin.site.register(Account, AccountAdmin)
admin.site.register(Profile, ProfileAdmin)

