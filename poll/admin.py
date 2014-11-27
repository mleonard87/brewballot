from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError

from poll.models import Poll, PollOption, Vote

class PollAdminForm(forms.ModelForm):
    def clean_is_active(self):
        currently_active = Poll.objects.filter(is_active=True).exclude(pk=self.instance.id).count()

        is_active = self.cleaned_data['is_active']

        if is_active and currently_active > 0:
            raise ValidationError('There can only be one active poll at a time.')
        else:
            return is_active

class PollAdmin(admin.ModelAdmin):
    form = PollAdminForm
    list_display = ("long_title", "is_active")
    exclude = ('slug',)

admin.site.register(Poll, PollAdmin)
admin.site.register(PollOption)
admin.site.register(Vote)