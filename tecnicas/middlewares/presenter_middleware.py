class PresenterAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        if path.startswith('/cata/presenter/'):
            technique = self.chechTypeTechnique(path)

            if not request.user.is_authenticated:
                return self.returuNoAutn(technique)

            if not hasattr(request.user, 'user_presentador'):
                return self.returuNoAutn(technique)

        return self.get_response(request)

    def returuNoAutn(self, technique=None):
        from django.shortcuts import redirect
        from django.urls import reverse
        from urllib.parse import urlencode

        base_url = reverse("cata_system:autenticacion")

        if technique:
            query_string = urlencode({"technique": technique})
            return redirect(f"{base_url}?{query_string}")

        return redirect(base_url)

    def chechTypeTechnique(self, path):
        if path.startswith('/cata/presenter/escalas'):
            return "escalas"
        elif path.startswith('/cata/presenter/rata'):
            return "rata"
        elif path.startswith('/cata/presenter/cata'):
            return "cata"
        elif path.startswith('/cata/presenter/perfil-ideal'):
            return "perfil-ideal"
        else:
            return None
