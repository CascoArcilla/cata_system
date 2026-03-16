from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from tecnicas.forms import CodesForm, ImagesProductForm
from utils import generarCodigos, delete_images, revisar_uso_cloudinary
import json
import cloudinary.uploader
import cloudinary.api


class PanelCodesController():
    def __init__(
        self,
        url_next: str = "cata_system:panel_configuracion_words",
        url_main: str = "cata_system:seleccion_tecnica",
        url_home: str = "cata_system:index",
        template: str = "create_sesion/conf-panel-codes.html"
    ):
        self.template = template
        self.url_next = url_next
        self.url_main = url_main
        self.url_home = url_home

    def getContext(
        self, form_codes, use_technique,
        select_technique, num_tester: int = None
    ):
        if select_technique == "general":
            self.url_main = "cata_system:seleccion_tecnica"
            self.url_home = "cata_system:index"

        context = {
            "form_codes": form_codes,
            "use_technique": use_technique,
            "url_main": reverse(self.url_main),
            "home_url": reverse(self.url_home)
        }

        if num_tester:
            context["num_tester"] = num_tester

        return context

    def controllGetEscalas(self, request: HttpRequest, data):
        """
        Obtain codes for scales technique
        Include orders for Catadores
        """
        num_products = data["numero_productos"]
        num_tester = data["numero_catadores"]

        codes_products = generarCodigos(num_products)

        form_codes = CodesForm(codes=codes_products)

        context = self.getContext(
            form_codes=form_codes,
            use_technique="escalas",
            select_technique=request.session.get("technique_selected"),
            num_tester=num_tester
        )

        return render(request, self.template, context)

    def controllPostEscalas(self, request: HttpRequest, data):
        """
        Post codes for scales technique
        Save orders for Catadores
        """
        num_tester = data["numero_catadores"]

        sorts_code = json.loads(request.POST.get("sort_codes"))
        codes = []

        for name, value in request.POST.items():
            if name.__contains__("producto_"):
                codes.append(value)

        form_codes = CodesForm(request.POST, codes=codes)

        context = self.getContext(
            form_codes=form_codes,
            use_technique="escalas",
            select_technique=request.session.get("technique_selected"),
            num_tester=num_tester
        )

        if form_codes.is_valid():
            codes_sort = {"product_codes": []}

            for name, value in form_codes.cleaned_data.items():
                codes_sort["product_codes"].append({name: value})

            codes_sort["sort_codes"] = sorts_code
            request.session["form_codes"] = codes_sort
            return redirect(reverse(self.url_next))
        else:
            self.context["error"] = "error en los datos recibidos"

        return render(request, self.template, self.context)

    def controllGetCata(self, request: HttpRequest, data, name_technique: str):
        """
        Obtain codes for CATA, this technique include images for products
        """
        num_products = data["numero_productos"]
        codes_products = generarCodigos(num_products)
        form_codes = CodesForm(codes=codes_products)
        form_images = ImagesProductForm(codes=codes_products)

        conf_basic = "cata_system:panel_configuracion_basic"

        technique_select = request.session.get("technique_selected")

        context = self.getContext(
            form_codes=form_codes,
            use_technique=name_technique,
            select_technique=technique_select
        )

        try:
            cloud_usage = revisar_uso_cloudinary()
            percentage = cloud_usage.get('percentage', 0)
            context["percentage_used"] = percentage
            if percentage >= 90:
                context["message"] = "Ya no es posible guardar más imágenes porque se alcanzó el 90% del límite de almacenamiento del servicio. Por favor borre sesiones con imágenes para liberar espacio."
        except Exception as e:
            print("Error al revisar uso de Cloudinary en GET:", e)

        context["form_images"] = form_images
        context["back_url"] = reverse(conf_basic) + "?name_tecnica=cata"

        return render(request, self.template, context)

    def controllPostCata(self, request: HttpRequest, data):
        """
        Post codes for CATA, this technique include images for products
        """
        codes = []

        for name, value in request.POST.items():
            if name.__contains__("producto_"):
                codes.append(value)

        form_codes = CodesForm(request.POST, codes=codes)
        form_images = ImagesProductForm(
            request.POST, files=request.FILES, codes=codes)

        if not form_codes.is_valid():
            context = self.getContext(
                form_codes=form_codes,
                use_technique="cata",
                select_technique=request.session.get("technique_selected")
            )
            context["form_images"] = form_images
            context["error"] = "error con los codigos"
            print("Error con los codigos")
            return render(request, self.template, context)

        if not form_images.is_valid():
            context = self.getContext(
                form_codes=form_codes,
                use_technique="cata",
                select_technique=request.session.get("technique_selected")
            )
            context["form_images"] = form_images
            context["error"] = "error con las imagenes, vuelve a seleccionar las imagenes"
            print("Error con las imagenes")
            return render(request, self.template, context)

        cleaned_codes = [value for name, value in form_codes.cleaned_data.items(
        ) if name.startswith('producto_')]
        uploaded_images = {}

        try:
            cloud_usage = revisar_uso_cloudinary()
            can_upload = cloud_usage.get('percentage', 0) < 90
        except Exception as e:
            print("Error al revisar uso de Cloudinary en POST:", e)
            can_upload = False

        try:
            values_codes = form_codes.cleaned_data.values()

            if can_upload:
                for original_code in codes:
                    new_code = True if original_code in values_codes else False
                    image_file = form_images.cleaned_data.get(
                        f'imagen_{original_code}')

                    if new_code and image_file:
                        upload_result = cloudinary.uploader.upload(
                            image_file,
                            folder='cata_system/uploads/',
                            transformation={'width': 1000,
                                            'crop': 'limit', 'quality': 'auto'}
                        )
                        uploaded_images[original_code] = upload_result['public_id']

        except Exception as e:
            if uploaded_images:
                delete_images(list(uploaded_images.values()))

            print("Error al subir las imágenes", e)

            context = self.getContext(
                form_codes=form_codes,
                use_technique="cata",
                select_technique=request.session.get("technique_selected")
            )

            context["form_images"] = form_images
            context["error"] = f"Error al subir las imágenes: {str(e)}"
            return render(request, self.template, context)

        request.session["form_codes"] = cleaned_codes
        request.session["form_images_cata"] = uploaded_images
        return redirect(reverse(self.url_next))

    def controllGetNoOrders(self, request: HttpRequest, data, name_technique: str):
        """
        Obtain codes for techniques without orders for Catadores
        """
        num_products = data["numero_productos"]
        codes_products = generarCodigos(num_products)
        form_codes = CodesForm(codes=codes_products)

        conf_basic = "cata_system:panel_configuracion_basic"

        technique_without_tags = {
            "perfil-flash": "?name_tecnica=perfil flash",
            "sort": "?name_tecnica=sort",
            "napping": "?name_tecnica=napping",
            "perfil-ideal": "?name_tecnica=perfil_ideal",
            "cata": "?name_tecnica=cata"
        }

        technique_select = request.session.get("technique_selected")

        context = self.getContext(
            form_codes=form_codes,
            use_technique=name_technique,
            select_technique=technique_select
        )

        if technique_select in technique_without_tags:
            context["back_url"] = reverse(
                conf_basic) + technique_without_tags[technique_select]

        return render(request, self.template, context)

    def controllPostNoOrders(self, request: HttpRequest, name_technique: str):
        """
        Post codes for techniques without orders for Catadores
        Save codes and redirect to words panel or vocabulary panel
        """
        codes = []

        for name, value in request.POST.items():
            if name.__contains__("producto_"):
                codes.append(value)

        form_codes = CodesForm(request.POST, codes=codes)

        if form_codes.is_valid():
            # Extract codes from cleaned_data to ensure uppercase conversion
            cleaned_codes = [value for name, value in form_codes.cleaned_data.items(
            ) if name.startswith('producto_')]
            request.session["form_codes"] = cleaned_codes
            return redirect(reverse(self.url_next))

        else:
            context = self.getContext(
                form_codes=form_codes,
                use_technique=name_technique,
                select_technique=request.session.get("technique_selected")
            )
            context["error"] = "error en los datos recibidos"

        return render(request, self.template, context)
