from ...models import Calificacion
from ...controllers import CalificacionController, DatoController


class ApiRatingController():
    def __init__(self, _rating_controller: CalificacionController, _data_controller: DatoController):
        self.rating_controller = _rating_controller
        self.data_controller = _data_controller
