from django.shortcuts import render

def autentication(req):
    return render(req, "tecnicas/auth.html")