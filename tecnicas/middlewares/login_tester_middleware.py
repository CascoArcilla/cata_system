from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse


class LoginTesterMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, req: HttpRequest):
        urls_protected = ["/cata/catador-main"]

        if req.path in urls_protected:
            if not "cata_username" in req.session:
                return redirect(reverse("cata_system:catador_login"))

        response = self.get_response(req)

        return response
