from django.shortcuts import render

def sesionesPanel(req):
    elementos = []

    for i in range(6):
        elementos.append(Elemento("Sesion " + str(i+1), "Hoy", "Convencional"))

    return render(req, "tecnicas/sesiones-panel.html", context={"elementos":elementos})

# Auxiliar classes
class Elemento():
    def __init__(self, nombre, fecha, tecnica):
        self.nombre = nombre
        self.fecha = fecha
        self.tecnica = tecnica