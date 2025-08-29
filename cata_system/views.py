from django.http import HttpRequest
from django.shortcuts import redirect

def home(req: HttpRequest):
    return redirect('/cata/')