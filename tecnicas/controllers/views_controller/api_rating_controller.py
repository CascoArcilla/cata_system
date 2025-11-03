from ...controllers import CalificacionController, DatoController
from ...utils import controller_error


class ApiRatingController():
    def __init__(self, rating_controller: CalificacionController, data_controller: DatoController):
        self.rating_controller = rating_controller
        self.data_controller = data_controller

    def setRating(self) -> int | dict:
        repetition = self.rating_controller.setRepetition()
        if isinstance(repetition, dict):
            return controller_error(repetition["error"])
        return repetition

    def saveRating(self):
        rating = self.rating_controller.saveRating()
        if isinstance(rating, dict):
            return controller_error(rating["error"])
        return rating

    def setRatingInData(self):
        update_rating = self.data_controller.setRating(
            self.rating_controller.rating)
        if isinstance(update_rating, dict):
            return controller_error(update_rating["error"])
        return update_rating

    def saveData(self):
        data = self.data_controller.saveData()
        if isinstance(data, dict):
            return controller_error(data["error"])
        return data

    def setValueRating(self):
        self.data_controller.setInstanceValue()

    def saveValue(self):
        value = self.data_controller.saveValue()
        if isinstance(value, dict):
            return controller_error(value["error"])

    def controllPostScales(self) -> dict:
        validate = self.rating_controller.validateRating()
        if isinstance(validate, dict):
            return controller_error(validate["error"])

        reptition = self.setRating()
        if isinstance(reptition, dict):
            return controller_error(reptition["error"])

        rating = self.saveRating()
        if isinstance(rating, dict):
            return controller_error(rating["error"])

        rating_data = self.setRatingInData()
        if isinstance(rating_data, dict):
            return controller_error(rating_data["error"])

        data = self.saveData()
        if isinstance(data, dict):
            return controller_error(data["error"])

        value = self.setValueRating()
        if isinstance(value, dict):
            return controller_error(value["error"])
        
        value_save = self.saveValue()
        if isinstance(value_save, dict):
            return controller_error(value_save["error"])

        return {"message": "La calificación se ha guardado"}
