from django.shortcuts import render

def mainPanel(req):
    pres = Presente("1233MMAS092222", "Juan Mendez Salazar")
    return render(req, "tecnicas/main-panel.html", context={"presentador":pres})

# Auxiliar classes
class Presente():
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre