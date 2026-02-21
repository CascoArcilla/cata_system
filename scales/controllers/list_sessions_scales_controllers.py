from controllers import ListSessionsController, SesionController
from django.http import HttpRequest


class ListSessionsScalesController(ListSessionsController):
    def __init__(self):
        super().__init__(template_name="views/list-sessions.html")

    def getElements(self, req: HttpRequest, page: int):
        filters = {
            "creadoPor": req.user.user_presentador,
            "tecnica__tipo_tecnica__nombre_tecnica": "escalas"
        }

        elements = SesionController.getSessionsByCretor(
            user_name=req.user.username, page=page, filters=filters
        )

        return elements
