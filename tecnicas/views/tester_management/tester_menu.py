from django.shortcuts import render

def testerMenu(req):
    return render(req, "tecnicas/manage_tester/catadores-panel.html")