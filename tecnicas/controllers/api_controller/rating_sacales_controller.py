from .. import CalificacionController, DatoController
from ...utils import controller_error


class RatingScalesController():
    def __init__(self, rating_controller: CalificacionController, data_controller: DatoController):
        self.rating_controller = rating_controller
        self.data_controller = data_controller

    def controllPostScales(self) -> dict:
        self.data_controller.setRating(
            new_rating=self.rating_controller.rating
        )

        data = self.data_controller.saveData()
        if isinstance(data, dict):
            return controller_error(data["error"])

        self.data_controller.setValue()
        
        value_save = self.data_controller.saveValue()
        if isinstance(value_save, dict):
            return controller_error(value_save["error"])

        return {"message": "La calificación se ha guardado"}
