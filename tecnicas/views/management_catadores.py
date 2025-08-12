from django.shortcuts import render

def managementCatadores(req):
    return render(req, "tecnicas/manage_tester/catadores-panel.html")