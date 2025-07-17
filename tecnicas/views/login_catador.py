from django.shortcuts import render

def catadorLogin(req):
    return render(req, "tecnicas/cata-login.html")