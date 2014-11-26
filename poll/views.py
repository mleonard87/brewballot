from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.db.models import Count
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from poll.models import Poll, PollOption, Vote

from django_twilio.decorators import twilio_view
from twilio.twiml import Response

def poll_default(request):
    try:
        poll = Poll.objects.get(is_active=True)
        return redirect(reverse('poll_results', args=[poll.pk, poll.slug]))
    except Poll.DoesNotExist:
        return redirect('no_active_polls')   

def poll_results(request, poll_id, poll_slug):
    poll = get_object_or_404(Poll, pk=poll_id)

    poll_options = PollOption.objects.select_related().filter(poll=poll).annotate(vote_count=Count('vote')).order_by('-vote_count')

    # total_votes = Vote.objects.filter(poll_option__poll=poll).count()

    return render_to_response(
        'poll/result.html',
        context_instance=RequestContext(
            request,
            {
                'poll': poll, 'poll_options': poll_options,
                # 'total_votes': total_votes
            }
            )
        )

@twilio_view
def sms_inbound(request):
    r = Response()

    body = request.GET.get('Body')
    sender = request.GET.get('From')

    if body.lower() == 'help':
        r.message(poll.long_title)
        return r

    if body.lower() == 'help':
        r.message(poll.long_title)
        return r

    try:
        poll = Poll.objects.get(is_active=True)

        try:
            poll_option = PollOption.objects.get(poll=poll, title__iexact=body)

            try:
                existing_vote = Vote.objects.get(
                    poll_option__poll=poll, sender_number=sender
                    )

                if existing_vote.poll_option.title.lower() == body.lower():
                    r.message("You've already voted for %s. You're drunk!" % body)
                    return r
                else: 
                    existing_vote.poll_option = poll_option
                    existing_vote.save()
                    r.message(u'Your vote has been updated! Cheers. \U0001F37B')
                    return r

            except Vote.DoesNotExist:
                vote = Vote()
                vote.poll_option = poll_option
                vote.sender_number = sender
                vote.save()
                r.message(u'Thanks for your vote! Cheers. \U0001F37B')
                return r

        except PollOption.DoesNotExist:
            r.message('How drunk are you? That option does not exist!')
            return r

    except Poll.DoesNotExist:
        r.message('You must be drunk, there are no open polls!')
        return r


    