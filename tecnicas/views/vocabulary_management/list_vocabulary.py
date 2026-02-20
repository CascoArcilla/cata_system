from django.http import HttpRequest
from controllers import ListVocabularyController


def listVocabulary(req: HttpRequest, num_page: int):
    controll_view = ListVocabularyController()
    if req.method == "GET":
        response = controll_view.controllGet(req, num_page)
        return response
    else:
        pass
