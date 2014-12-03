from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.db.models import Count
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.conf import settings

from poll.models import Poll, PollOption, Vote

from django_twilio.decorators import twilio_view
from twilio.twiml import Response

import json

def poll_default(request):
    try:
        poll = Poll.objects.get(is_active=True)
        return redirect(reverse('poll_results', args=[poll.pk, poll.slug]))
    except Poll.DoesNotExist:
        return redirect('no_active_polls')   

def poll_results(request, poll_id, poll_slug):
    poll = get_object_or_404(Poll, pk=poll_id)

    poll_options = PollOption.objects.select_related().filter(poll=poll).annotate(vote_count=Count('vote'))

    max_vote = PollOption.objects.select_related().filter(poll=poll).annotate(vote_count=Count('vote')).order_by('-vote_count')[0].vote_count

    # total_votes = Vote.objects.filter(poll_option__poll=poll).count()

    return render_to_response(
        'poll/result.html',
        context_instance=RequestContext(
            request,
            {
                'poll': poll, 'poll_options': poll_options,
                'max_vote': max_vote, 'sms_number': settings.VOTE_SMS_NUMBER
            }
            )
        )

def poll_refresh(request, poll_id, poll_slug):
    poll = get_object_or_404(Poll, pk=poll_id)

    poll_options = PollOption.objects.select_related().filter(poll=poll).annotate(vote_count=Count('vote')).order_by('-vote_count')

    refresh_dict = {'max_votes': poll_options[0].vote_count}
    for po in poll_options:
        refresh_dict[po.title] = po.vote_count

    return HttpResponse(json.dumps(refresh_dict), content_type='application/json')

def sms_response_success(message):
    r = Response()
    r.message(u"%s\n\nFor more information reply to this SMS with POLLHELP." % message)
    return r

def sms_response_error(message):
    r = Response()
    r.message(u"%s\n\nFor more information reply to this SMS with POLLHELP." % message)
    return r

def sms_response_help(poll_title, poll_options):
    r = Response()
    r.message(
        u"%s\nOptions: %s.\n\nReply to this SMS with your vote!\n\nTo see the results text RESULTS.\n\nTo remove a vote text UNVOTE. \U0001F37A" % (
            poll_title, poll_options
            )
        )
    return r


@twilio_view
def sms_inbound(request):
    body = request.POST.get('Body', '')
    sender = request.POST.get('From', '')

    print body
    print body.lower()
    print request.POST

    try:
        poll = Poll.objects.get(is_active=True)

        if body.lower() == 'pollhelp':

            poll_options = ', '.join(
                p.title for p in PollOption.objects.filter(poll=poll)
                )

            return sms_response_help(
                poll_title=poll.long_title, poll_options=poll_options
                )

        if body.lower() == 'results' or body.lower() == 'result':
            votes = PollOption.objects.select_related().filter(poll=poll).annotate(vote_count=Count('vote')).order_by('-vote_count')

            votes_text = '\n'.join(v.title + ': ' + unicode(v.vote_count) for v in votes)

            return sms_response_success(
                u"Results for: \"%s\"\n\n%s" % (poll.long_title, votes_text)
                )

        if body.lower() == 'unvote':
            try:
                vote = Vote.objects.get(
                    poll_option__poll=poll, sender_number=sender
                    )
                vote.delete()

                return sms_response_success(
                    u"Your vote has been removed! \U0001F631"
                    )

            except Vote.DoesNotExist:
                return sms_response_error(
                    u"Clearly you're drunk - you can't unvote if you haven't even voted yet! \U0001F632"
                    )           

        try:
            poll_option = PollOption.objects.get(poll=poll, title__iexact=body)

            try:
                existing_vote = Vote.objects.get(
                    poll_option__poll=poll, sender_number=sender
                    )

                if existing_vote.poll_option.title.lower() == body.lower():
                    return sms_response_error(
                        u"You've already voted for %s. You're drunk! \U0001F632" % body
                        )
                else: 
                    existing_vote.poll_option = poll_option
                    existing_vote.save()

                    return sms_response_success(
                        u"Your vote has been updated! Cheers. \U0001F37B"
                        )

            except Vote.DoesNotExist:
                vote = Vote()
                vote.poll_option = poll_option
                vote.sender_number = sender
                vote.save()

                return sms_response_success(
                    u"Thanks for your vote! Cheers. \U0001F37B"
                    )

        except PollOption.DoesNotExist:
            return sms_response_error(
                u"How drunk are you? That option does not exist! \U0001F632"
                )

    except Poll.DoesNotExist:
        return sms_response_error(
            u"You must be drunk, there are no open polls! \U0001F632"
            )

    return sms_response_error(
        u"What happened?! \U0001F632"
        )