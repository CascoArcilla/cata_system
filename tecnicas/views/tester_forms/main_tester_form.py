from django.http import HttpRequest, JsonResponse
from django.shortcuts import render


def mainTesterForm(req: HttpRequest):
    if req.method == "POST":
        return render(req, "tecnica/forms_tester/main_tester.html")
    else:
        return JsonResponse({"error": "metodo no permitido"})
