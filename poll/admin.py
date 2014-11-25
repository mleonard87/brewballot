from django.contrib import admin
from poll.models import Poll, PollOption, Vote

class PollAdmin(admin.ModelAdmin):
    exclude = ('slug',)

admin.site.register(Poll, PollAdmin)
admin.site.register(PollOption)
admin.site.register(Vote)