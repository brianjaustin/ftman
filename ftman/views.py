from django.http import HttpResponse

from ftman import settings


def acme_challenge(request, _):
    """
    ACME challenge response for LetsEncrypt.

    """
    return HttpResponse(settings.ACME_CHALLENGE_CONTENT)
