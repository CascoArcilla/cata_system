from django.http import HttpRequest
from django.shortcuts import render
from ...controllers import SesionController


def sesionsPanel(req: HttpRequest, page: int):
    context = {"num_page": page}

    response = SesionController.getSessionsSavesByCretor(
        user_name=req.user.username, page=page)

    if isinstance(response, dict):
        context["error"] = response["error"]
        return render(req, "tecnicas/manage_sesions/sesiones-panel.html", context=context)
    
    (sessions_in_page, is_last_page, current_page) = response

    context["sessions"] = sessions_in_page
    context["last_page"] = is_last_page
    context["num_paginas"] = current_page

    return render(req, "tecnicas/manage_sesions/sesiones-panel.html", context=context)
