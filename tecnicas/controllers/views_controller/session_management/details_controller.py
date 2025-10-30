from tecnicas.models import SesionSensorial, Presentador, Tecnica
from tecnicas.utils import controller_error


class DetallesController():
    url_template = "tecnicas/manage_sesions/detalles-sesion.html"

    def __init__(self, session: SesionSensorial):
        self.session = session

    def deleteSesorialSession(self):
        technique = Tecnica.objects.get(id=self.session.tecnica.id)
        technique.delete()