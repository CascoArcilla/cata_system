from django.http import HttpRequest
from ..utils import general_error

def configuracionPanelWords(req: HttpRequest):
    if req.method == "GET":
        return general_error("This endpoint is not implemented yet.")
    else:
        return general_error("Method not allowed.")