import datetime
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import TestCase
from Polls.models import Poll

def create_poll(question, days):
    """
    Create Poll with given 'question' published given 'days' from now
    """
    return Poll.objects.create(question=question,
                               pub_date=timezone.now() + datetime.timedelta(days=days))


class PollMethodTests(TestCase):
    def test_was_published_recently_with_future_poll(self):
        """
        Return False for polls that are in the future
        """
        future_poll = Poll(pub_date=timezone.now() + datetime.timedelta(days=30))
        self.assertEqual(future_poll.was_published_recently(), False)

    def test_was_published_recently_with_old_poll(self):
        """
        Return False for polls older than 1 day from now
        """
        old_poll = Poll(pub_date=timezone.now() - datetime.timedelta(days=30))
        self.assertEqual(old_poll.was_published_recently(), False)

    def test_was_published_recently_with_recent_poll(self):
        """
        Return True for polls that were published within the last day
        """
        recent_poll = Poll(pub_date=timezone.now() - datetime.timedelta(hours=1))
        self.assertEqual(recent_poll.was_published_recently(), True)


class PollViewTests(TestCase):
    def test_index_view_with_no_polls(self):
        """
        Display appropriate message when no polls exist
        """
        response = self.client.get(reverse('Polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            []
        )

    def test_index_view_with_a_past_poll(self):
        """
        Display poll published in the past on index page
        """
        create_poll(question='Past poll.', days=-30)
        response = self.client.get(reverse('Polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Poll: Past poll.>']
        )

    def test_index_view_with_a_future_poll(self):
        """
        Do not display poll published in the future on index page
        """
        create_poll(question='Future poll.', days=30)
        response = self.client.get(reverse('Polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            []
        )

    def test_index_view_with_future_and_past_poll(self):
        """
        Display only polls published in the past, even if both exist
        """
        create_poll(question='Past poll.', days=-30)
        create_poll(question='Future poll.', days=30)
        response = self.client.get(reverse('Polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Poll: Past poll.>']
        )

    def test_index_view_with_two_past_polls(self):
        """
        Display multiple polls on index page if possible
        """
        create_poll(question='Past poll 1.', days=-30)
        create_poll(question='Past poll 2.', days=-5)
        response = self.client.get(reverse('Polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Poll: Past poll 2.>', '<Poll: Past poll 1.>']
        )


class PollIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_poll(self):
        """
        Return 404 if poll is in the future
        """
        future_poll = create_poll(question='Future poll.', days=5)
        response = self.client.get(reverse('Polls:detail', args=(future_poll.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_poll(self):
        """
        Display poll details if poll was published in the past
        """
        past_poll = create_poll(question='Past poll.', days=-5)
        response = self.client.get(reverse('Polls:detail', args=(past_poll.id,)))
        self.assertContains(response, past_poll.question, status_code=200)


class PollIndexResultsTests(TestCase):
    def test_results_view_with_a_future_poll(self):
        """
        Return 404 if poll is in the future
        """
        future_poll = create_poll(question='Future poll.', days=5)
        response = self.client.get(reverse('Polls:results', args=(future_poll.id,)))
        self.assertEqual(response.status_code, 404)

    def test_results_view_with_a_past_poll(self):
        """
        Display poll results if poll was published in the past
        """
        past_poll = create_poll(question='Past poll.', days=-5)
        response = self.client.get(reverse('Polls:results', args=(past_poll.id,)))
        self.assertContains(response, past_poll.question, status_code=200)
