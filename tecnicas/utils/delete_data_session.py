from django.http import HttpRequest
from tecnicas.constants import FORMS_TO_CREATE_SESSION
from .personal_errors import general_error


def deleteDataSession(request: HttpRequest):
    for key in FORMS_TO_CREATE_SESSION:
        if key in request.session:
            del request.session[key]
    return True
