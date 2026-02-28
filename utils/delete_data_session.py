from django.http import HttpRequest
from tecnicas.constants import FORMS_TO_CREATE_SESSION


def deleteDataSession(request: HttpRequest):
    for key in FORMS_TO_CREATE_SESSION:
        if key in request.session:
            del request.session[key]
    return True
