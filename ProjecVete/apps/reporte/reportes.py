import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.utils import timezone, dates
from django.db.models import Avg
from django.db.models import Sum
from django.db.models.functions import ExtractMonth,TruncMonth
from django.db.models import Count
import datetime

from apps.venta.models import FacturaBody,FacturaHeader
from apps.regmedic.models import Cliente, Mascota, Consulta, Vacuna, Despa
from apps.inv.models import Producto


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, "/media/"))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path

#VENTAS
def reportventa_all(request):
    template_path= 'reporte/report_venta_all.html'
    today = timezone.now()

    ventas = FacturaBody.objects.all().order_by('-factura__fecha')
    context = {
        'obj':ventas,
        'today':today,
        'request':request
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Todas las Ventas.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

#CLIENTES
def reportcliente_all(request):
    template_path= 'reporte/report_cliente_all.html'
    today = timezone.now()

    cliente = Cliente.objects.filter(estado = True)
    context = {
        'obj':cliente,
        'today':today,
        'request':request
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Todas los Clientes.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

#MASCOTA
def reportmascota_all(request):
    template_path= 'reporte/report_mascota_all.html'
    today = timezone.now()

    mascota = Mascota.objects.filter(estado = True)
    context = {
        'obj':mascota,
        'today':today,
        'request':request
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Todas las macotas.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

#PRODUCTOS
def reportproducto_all(request):
    template_path= 'reporte/report_producto_all.html'
    today = timezone.now()

    producto = Producto.objects.filter(estado = True)
    context = {
        'obj':producto,
        'today':today,
        'request':request
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Todas los productos.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def reportclient_one (request, cedula):
    template_path = 'reporte/report_cliente_one.html'
    today = timezone.now

    cliente = Cliente.objects.filter(pk = cedula).first()
    mascota = Mascota.objects.filter(cliente = cedula)
    context = {
        'obj':cliente,
        'mascota':mascota,
        'today':today,
        'request':request
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Detalle del cliente.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def reportmascot_one (request, id):
    template_path = 'reporte/report_mascota_one.html'
    today = timezone.now

    mascota = Mascota.objects.filter(pk = id).first()
    consulta = Consulta.objects.filter(mascota = id)
    desparasitacion = Despa.objects.filter(mascota = id)
    vacunacion = Vacuna.objects.filter(mascota = id)


    context = {
        'mascota':mascota,
        'consulta':consulta,
        'vacuna':vacunacion,
        'despa':desparasitacion,
        'today':today,
        'request':request
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Detalle de la mascota.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response