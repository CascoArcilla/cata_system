from django.http import HttpRequest
from django.shortcuts import render

def configuracionPanelTags(req: HttpRequest):
    return render(req, "tecnicas/configuracion-panel-tags.html")