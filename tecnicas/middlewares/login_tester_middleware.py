from django.http import HttpRequest


class LoginTesterMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, req: HttpRequest):
        url_protected = "/cata/testers/"

        if req.path.startswith(url_protected):
            if not "cata_username" in req.session:
                from django.shortcuts import redirect
                from django.urls import reverse
                return redirect(reverse("cata_system:catador_login"))

        response = self.get_response(req)

        return response
