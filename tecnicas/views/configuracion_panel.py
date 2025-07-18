from django.shortcuts import render

def configuracionPanel(req):
    return render(req, "tecnicas/configuracion-panel.html")