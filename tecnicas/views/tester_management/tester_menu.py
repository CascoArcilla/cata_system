from django.shortcuts import render
from django.urls import reverse

def testerMenu(req):
    url_home = req.session.get("sensorial_url_main")
    return render(req, "manage_tester/testers-panel.html", {"url_home": reverse(url_home)})