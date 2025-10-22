from django.http import HttpRequest
from django.shortcuts import render
from ...controllers import SesionController


def sesionsPanel(req:HttpRequest, page: int):
    context = {"num_page": page}

    (sessions_in_page, last_page) = SesionController.getSessionsSavesByCretor(
        user_name=req.user.username, page=page)

    if isinstance(sessions_in_page, dict):
        context["error"] = sessions_in_page["error"]
        return render(req, "tecnicas/manage_sesions/sesiones-panel.html", context=context)

    context["sessions"] = sessions_in_page
    context["last_page"] = last_page

    number_pages = SesionController.getNumberSessionsByCreator(
        user_name=req.user.username)
    if isinstance(number_pages, dict):
        context["num_paginas"] = sessions_in_page["error"]
        return render(req, "tecnicas/manage_sesions/sesiones-panel.html", context=context)

    context["num_paginas"] = number_pages

    return render(req, "tecnicas/manage_sesions/sesiones-panel.html", context=context)
