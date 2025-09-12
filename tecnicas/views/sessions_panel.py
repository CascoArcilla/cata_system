from django.shortcuts import render
from ..controllers import SesionController


def sesionsPanel(req, page: int):
    context = {}

    sessions_in_page = SesionController.getSessionsSavesByCretor(
        user_name="aguBido", page=page)

    if isinstance(sessions_in_page, dict):
        context["error"] = sessions_in_page["error"]
        return render(req, "tecnicas/manage_sesions/sesiones-panel.html", context=context)

    context["sessions"] = sessions_in_page

    number_pages = SesionController.getNumberSessionsByCreator(
        user_name="aguBido")
    if isinstance(number_pages, dict):
        context["num_paginas"] = sessions_in_page["error"]
        return render(req, "tecnicas/manage_sesions/sesiones-panel.html", context=context)

    context["num_paginas"] = number_pages

    return render(req, "tecnicas/manage_sesions/sesiones-panel.html", context=context)