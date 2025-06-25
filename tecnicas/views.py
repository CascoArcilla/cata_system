from django.shortcuts import render
import array as ar

# Create your views here.
def mainPanel(req):
    pres = Presente("1233MMAS092222", "Juan Mendez Salazar")
    return render(req, "tecnicas/main-panel.html", context={"presentador":pres})

def autentication(req):
    return render(req, "tecnicas/auth.html")

def catadorLogin(req):
    return render(req, "tecnicas/cata-login.html")

def managementCatadores(req):
    return render(req, "tecnicas/catadores-panel.html")

def sesionesPanel(req):
    return render(req, "tecnicas/sesiones-panel.html")

def selecionTecnica(req):
    
    elementos = ["Par", "lo", "asa", "miua", "guau", "mal", "pollo", "yuo", "ui", "ua"]
    return render(req, "tecnicas/seleccion-tecnica.html", context={"elementos":elementos})

class Presente():
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre