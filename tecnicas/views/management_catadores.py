from django.shortcuts import render

def managementCatadores(req):
    return render(req, "tecnicas/catadores-panel.html")