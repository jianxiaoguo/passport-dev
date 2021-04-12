"""
Helper functions used by the Drycc Passport server.
"""
import logging
import datetime
import time
import six

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.cache import cache

logger = logging.getLogger(__name__)


def get_user_by_name(username):
    return cache.get_or_set(f'user_{username}',
                            lambda: _get_user(username),
                            5 * 60)


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


def get_local_host(request):
    uri = request.build_absolute_uri()
    return uri[0:uri.find(request.path)]


def _get_user(username):
    from django.contrib.auth.models import User
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise
    return user


def date2timestamp(date):
    if not isinstance(date, datetime.date):
        raise
    return time.mktime(date.timetuple())


def datetime2timestamp(dt):
    if not isinstance(dt, datetime.datetime):
        raise
    return dt.timestamp()


def timestamp2datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
