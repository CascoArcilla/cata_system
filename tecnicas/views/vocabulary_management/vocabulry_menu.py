from django.shortcuts import render

def vocabularyMenu(req):
    return render(req, "tecnicas/manage_vocabulary/panel-vocabulary.html")