from django.http import HttpRequest
from django.shortcuts import render

def configurationsPanelWords(req:HttpRequest):
    return render(req, "tecnicas/configuracion-panel-palabras.html")