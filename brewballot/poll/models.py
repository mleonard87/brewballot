from django.db import models
from django.template.defaultfilters import slugify

class Poll(models.Model):
    long_title = models.CharField(max_length=100)
    short_title = models.CharField(max_length=30)
    slug = models.SlugField(max_length=50)
    is_active = models.BooleanField(default=False)
    created_on = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            # Newly created object, so set slug
            self.slug = slugify(self.short_title)

        super(Poll, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.long_title

class PollOption(models.Model):
    poll = models.ForeignKey(Poll)
    title = models.CharField(max_length=10)
    created_on = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return '%s -- %s' % (self.poll.short_title, self.title)

class Vote(models.Model):
    poll_option = models.ForeignKey(PollOption)
    sender_number = models.CharField(max_length=20)
    created_on = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('poll_option', 'sender_number')

    def __unicode__(self):
        return '%s -- %s (%s)' % (self.poll_option.poll.short_title, 
            self.poll_option.title, self.sender_number
            )
