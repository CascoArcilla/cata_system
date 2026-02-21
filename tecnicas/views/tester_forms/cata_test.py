from django.http import HttpRequest
from tecnicas.models import SesionSensorial
from controllers import TestCataController


def cataTest(req: HttpRequest, code_sesion: str):
    if req.method == "GET":
        session = SesionSensorial.objects.get(codigo_sesion=code_sesion)
        controll_view = TestCataController(
            sensorial_session=session, user_tester=req.user.user_catador)
        return controll_view.controllGet(request=req)
