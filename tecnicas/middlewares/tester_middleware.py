# usuarios/middleware/catador_middleware.py
from django.core.exceptions import PermissionDenied


class TesterAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        if path.startswith('/cata/testers/'):
            if not request.user.is_authenticated:
                from django.shortcuts import redirect
                return redirect("cata_system:catador_login")

            if not hasattr(request.user, 'user_catador'):
                return redirect("cata_system:catador_login")

        return self.get_response(request)

# from django.http import HttpRequest


# class LoginTesterMiddleware():
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, req: HttpRequest):
#         base_url_protected = "/cata/testers/"

#         if req.path.startswith(base_url_protected):
#             if not "cata_username" in req.session:
#                 id_participacion = req.COOKIES.get("id_participacion")
#                 if id_participacion:
#                     from tecnicas.controllers import ParticipacionController
#                     ParticipacionController.outSession(id_participacion)
#                 from django.shortcuts import redirect
#                 from django.urls import reverse
#                 response = redirect(reverse("cata_system:catador_login"))
#                 response.delete_cookie("id_participacion")
#                 return response

#         response = self.get_response(req)

#         return response
