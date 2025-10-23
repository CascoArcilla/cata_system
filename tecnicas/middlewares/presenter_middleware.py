class PresenterAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        if path.startswith('/cata/presenter/'):
            if not request.user.is_authenticated:
                from django.shortcuts import redirect
                return redirect("cata_system:autenticacion")

            if not hasattr(request.user, 'user_presentador'):
                from django.shortcuts import redirect
                return redirect("cata_system:autenticacion")

        return self.get_response(request)
