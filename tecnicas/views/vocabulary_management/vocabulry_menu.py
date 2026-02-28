from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse


def vocabularyMenu(req: HttpRequest) -> HttpResponse:
    url_home = req.session.get("sensorial_url_main")

    context_view = {
        "url_home": reverse(url_home),
    }

    return render(req, "manage_vocabulary/panel-vocabulary.html", context_view)
