from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from tecnicas.controllers import SesionController


def sesionsList(req: HttpRequest, page: int):
    if req.method == "GET":
        return get_sessions_list(req, page)
    else:
        return JsonResponse({"message": "Método no permitido"})


def get_sessions_list(
    req: HttpRequest, page: int, filters: dict = {},
    template: str = "tecnicas/list_sessions/sessions-panel.html"
):
    context = {
        "num_page": page
    }

    response = SesionController.getSessionsSavesByCretor(
        user_name=req.user.username, page=page, more_filter=filters)

    if isinstance(response, dict):
        context["error"] = response["error"]
        return render(req, template, context=context)

    (sessions_in_page, is_last_page, current_page) = response

    context["sessions"] = sessions_in_page
    context["last_page"] = is_last_page
    context["num_paginas"] = current_page

    if "message" in req.GET:
        context["message"] = req.GET.get("message")

    return render(req, template, context=context)
