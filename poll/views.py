from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db.models import Count

from poll.models import Poll, PollOption #, Vote

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