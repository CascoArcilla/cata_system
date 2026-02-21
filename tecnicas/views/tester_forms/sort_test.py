from django.http import HttpRequest
from tecnicas.models import SesionSensorial
from controllers import TestSortController
from utils import noValidTechnique


def sortTest(req: HttpRequest, code_sesion: str):
    if req.method == "GET":
        session = SesionSensorial.objects.get(codigo_sesion=code_sesion)
        controll_view = TestSortController(
            sensorial_session=session, user_tester=req.user.user_catador)
        return controll_view.controllGet(request=req)

    elif req.method == "POST":
        session = SesionSensorial.objects.get(codigo_sesion=code_sesion)
        controll_view = TestSortController(
            sensorial_session=session, user_tester=req.user.user_catador)
        return controll_view.controllPost(request=req)
        
    else:
        return noValidTechnique(
            name_view="cata_system:catador_init_session",
            query_params={
                "error": "Método no valido"
            }
        )
