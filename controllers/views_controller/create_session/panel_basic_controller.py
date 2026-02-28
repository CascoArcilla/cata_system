from tecnicas.forms import SesionBasicForm, SesionBasicCATAForm, SesionBasicPFForm, SesionBasicSortForm, SesionBasicNappingForm, SesionBasicRATAForm, SesionBasicIdealForm
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse


class PanelBasicController():
    conf_initial_rata = {
        "numero_catadores": 0,
        "numero_repeticiones": 1
    }

    def __init__(self, url_main: str = "cata_system:seleccion_tecnica", url_home: str = "cata_system:index"):
        self.template = "tecnicas/create_sesion/conf-panel-basic.html"
        self.url_conf_tags = "cata_system:panel_configuracion_tags"
        self.url_conf_codes = "cata_system:panel_configuracion_codes"
        self.url_main = url_main
        self.url_home = url_home

    def getContext(self, form_sesion, use_technique, select_technique):
        if select_technique == "general":
            url_main = "cata_system:seleccion_tecnica"
            url_home = "cata_system:index"
        else:
            url_main = self.url_main
            url_home = self.url_home

        return {
            "form_sesion": form_sesion,
            "use_technique": use_technique,
            "url_main":  reverse(url_main),
            "home_url": reverse(url_home)
        }

    def controllGetEscalas(self, request: HttpRequest):
        form_sesion = SesionBasicForm()

        view_context = self.getContext(
            form_sesion=form_sesion,
            use_technique="escalas",
            select_technique=request.session.get("select_technique")
        )

        response = render(
            request, self.template, view_context)
        return response

    def controllPostEscalas(self, request: HttpRequest, name_tecnica: str):
        try:
            form = SesionBasicForm(request.POST)

            if form.is_valid():
                values = {}
                for name, value in form.cleaned_data.items():
                    if name == "tipo_escala":
                        values[name] = value.id
                    else:
                        values[name] = value

                values["name_tecnica"] = name_tecnica
                request.session['form_basic'] = values
                response = redirect(
                    reverse(self.url_conf_tags))

            else:
                view_context = self.getContext(
                    form_sesion=form,
                    use_technique="escalas",
                    select_technique=request.session.get("select_technique")
                )

                view_context["error"] = "Información no valida"
                response = render(request, self.template, view_context)

        except KeyError:
            url_main = reverse(self.default_url_main) if request.session.get(
                "technique_selected") != "escalas" else reverse("cata_system:index_escalas")
            response = redirect(
                url_main + "?error=error en datos de configuracion")

        return response

    def controllGetRATA(self, request: HttpRequest):
        form_sesion = SesionBasicRATAForm()

        view_context = self.getContext(
            form_sesion=form_sesion,
            use_technique="rata",
            select_technique=request.session.get("select_technique")
        )

        response = render(
            request, self.template, view_context)
        return response

    def controllPostRATA(self, request: HttpRequest, name_tecnica: str):
        try:
            form = SesionBasicRATAForm(request.POST)

            if form.is_valid():
                values = {}
                for name, value in form.cleaned_data.items():
                    if name == "tipo_escala":
                        values[name] = value.id
                    else:
                        values[name] = value

                if form.errors:
                    response = render(request, self.template, {
                        "form_sesion": form, "error": "No puedes modificar el número de catadores o repeticiones", "use_technique": "rata"})
                else:
                    values["name_tecnica"] = name_tecnica
                    request.session['form_basic'] = values
                    response = redirect(
                        reverse(self.url_conf_tags))
            else:
                view_context = self.getContext(
                    form_sesion=form,
                    use_technique="rata",
                    select_technique=request.session.get("select_technique")
                )

                view_context["error"] = "Información no valida"
                response = render(request, self.template, view_context)

        except KeyError:
            response = redirect(reverse(
                self.url_main) + "?error=error en datos de configuracion")

        return response

    def controllGetCATA(self, request: HttpRequest):
        form_sesion = SesionBasicCATAForm()

        view_context = self.getContext(
            form_sesion=form_sesion,
            use_technique="cata",
            select_technique=request.session.get("select_technique")
        )

        return render(
            request, self.template, view_context)

    def controllPostCATA(self, request: HttpRequest, name_tecnica: str):
        form = SesionBasicCATAForm(request.POST)

        if form.is_valid():
            values = {}
            for name, value in form.cleaned_data.items():
                values[name] = value

            values["name_tecnica"] = name_tecnica
            request.session['form_basic'] = values
            response = redirect(
                reverse(self.url_conf_codes))
        else:
            view_context = self.getContext(
                form_sesion=form,
                use_technique="cata",
                select_technique=request.session.get("select_technique")
            )

            view_context["error"] = "Información no valida"
            response = render(request, self.template, view_context)

        return response

    def controllGetPF(self, request: HttpRequest):
        form_sesion = SesionBasicPFForm()

        view_context = self.getContext(
            form_sesion=form_sesion,
            use_technique="perfil flash",
            select_technique=request.session.get("select_technique")
        )

        return render(
            request, self.template, view_context)

    def controllPostPF(self, request: HttpRequest, name_tecnica: str):
        form = SesionBasicPFForm(request.POST)

        if form.is_valid():
            values = {}
            for name, value in form.cleaned_data.items():
                values[name] = value

            values["name_tecnica"] = name_tecnica
            request.session['form_basic'] = values
            response = redirect(
                reverse(self.url_conf_codes))
        else:
            view_context = self.getContext(
                form_sesion=form,
                use_technique="perfil flash",
                select_technique=request.session.get("select_technique")
            )

            view_context["error"] = "Información no valida"
            response = render(request, self.template, view_context)

        return response

    def controllGetSort(self, request: HttpRequest):
        form_sesion = SesionBasicSortForm()

        view_context = self.getContext(
            form_sesion=form_sesion,
            use_technique="sort",
            select_technique=request.session.get("select_technique")
        )

        return render(
            request, self.template, view_context)

    def controllPostSort(self, request: HttpRequest, name_tecnica: str):
        form = SesionBasicSortForm(request.POST)

        if form.is_valid():
            values = {}
            for name, value in form.cleaned_data.items():
                values[name] = value

            values["name_tecnica"] = name_tecnica
            request.session['form_basic'] = values
            response = redirect(
                reverse(self.url_conf_codes))
        else:
            view_context = self.getContext(
                form_sesion=form,
                use_technique="sort",
                select_technique=request.session.get("select_technique")
            )

            view_context["error"] = "Información no valida"
            response = render(request, self.template, view_context)

        return response

    def controllGetNapping(self, request: HttpRequest):
        form_sesion = SesionBasicNappingForm()

        view_context = self.getContext(
            form_sesion=form_sesion,
            use_technique="napping",
            select_technique=request.session.get("select_technique")
        )

        return render(
            request, self.template, view_context)

    def controllPostNapping(self, request: HttpRequest, name_tecnica: str):
        form = SesionBasicNappingForm(request.POST)

        if form.is_valid():
            values = {}
            for name, value in form.cleaned_data.items():
                values[name] = value

            values["name_tecnica"] = name_tecnica
            request.session['form_basic'] = values
            response = redirect(
                reverse(self.url_conf_codes))
        else:
            view_context = self.getContext(
                form_sesion=form,
                use_technique="napping",
                select_technique=request.session.get("select_technique")
            )

            view_context["error"] = "Información no valida"
            response = render(request, self.template, view_context)

        return response

    def controllGetIdeal(self, request: HttpRequest):
        form_sesion = SesionBasicIdealForm()

        view_context = self.getContext(
            form_sesion=form_sesion,
            use_technique="perfil_ideal",
            select_technique=request.session.get("select_technique")
        )

        return render(
            request, self.template, view_context)

    def controllPostIdeal(self, request: HttpRequest, name_tecnica: str):
        form = SesionBasicIdealForm(request.POST)

        if form.is_valid():
            values = {}
            for name, value in form.cleaned_data.items():
                values[name] = value

            values["name_tecnica"] = name_tecnica
            request.session['form_basic'] = values
            response = redirect(
                reverse(self.url_conf_codes))
        else:
            view_context = self.getContext(
                form_sesion=form,
                use_technique="perfil_ideal",
                select_technique=request.session.get("select_technique")
            )

            view_context["error"] = "Información no valida"
            response = render(request, self.template, view_context)

        return response
