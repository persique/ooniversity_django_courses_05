from django.contrib import admin
from .models import Coach


class CoachAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'gender', 'skype', 'description')
    list_filter = ['user__is_staff']
    def first_name(self, obj):
        return obj.user.first_name
    def last_name(self, obj):
        return obj.user.last_name


admin.site.register(Coach, CoachAdmin)
