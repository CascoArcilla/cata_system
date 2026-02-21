from django.http import HttpRequest
from django.shortcuts import render
from controllers import SesionController


class ListSessionsController():
    def __init__(self, template_name: str):
        self.template_name = template_name

    def getSessionByCreator(self, req: HttpRequest, page: int, all_sessions=False):
        context = {"num_page": page}

        if all_sessions:
            response = SesionController.getSessionsByCretor(
                user_name=req.user.user_presentador, page=page
            )
        else:
            response = self.getElements(req, page)

        if isinstance(response, dict):
            context["error"] = response["error"]
            return render(req, self.template_name, context=context)

        (sessions_in_page, is_last_page, current_page) = response

        context["sessions"] = sessions_in_page
        context["last_page"] = is_last_page
        context["num_paginas"] = current_page
        
        if "message" in req.GET:
            context["message"] = req.GET.get("message")

        return render(req, self.template_name, context=context)

    def getElements(self, req: HttpRequest, page: int):
        elements = SesionController.getSessionsByCretor(
            user_name=req.user.user_presentador, page=page
        )
        return elements
