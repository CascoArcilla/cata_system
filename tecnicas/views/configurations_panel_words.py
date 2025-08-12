from django.http import HttpRequest

def configuracionPanelWords(req: HttpRequest):
    if req.method == "GET":
        return error("This endpoint is not implemented yet.")
    else:
        return error("Method not allowed.")