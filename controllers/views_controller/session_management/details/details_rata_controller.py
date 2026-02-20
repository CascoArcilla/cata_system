from tecnicas.models import SesionSensorial
from .details_controller import DetallesController


class DetallesRATAController(DetallesController):
    def __init__(self, session: SesionSensorial):
        super().__init__(session)
