from django.http import HttpRequest
from controllers import ListVocabularyController
from utils import general_error


def listVocabulary(req: HttpRequest, num_page: int):
    url_home = req.session.get("sensorial_url_main")
    controll_view = ListVocabularyController(url_home=url_home)
    if req.method == "GET":
        response = controll_view.controllGet(req, num_page)
        return response
    else:
        get_response = general_error("Método no permitido")
        
