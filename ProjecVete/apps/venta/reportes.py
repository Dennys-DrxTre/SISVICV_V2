from django.shortcuts import render
import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.utils import timezone
from django.utils.dateparse import parse_date
from datetime import timedelta
from django.db.models import Sum

from .models import FacturaBody,FacturaHeader
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


def reportes_all(request):
    template_path= 'venta/reportes_all.html'
    today = timezone.now()
    todayD = str(timezone.now().day) + '-' + str(timezone.now().month) + '-' + str(timezone.now().year) 

    ventas = FacturaBody.objects.filter(factura__fecha = timezone.now())
    context = {
        'obj':ventas,
        'today':today,
        'request':request,
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="ventas_hoy({todayD}).pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def reporte_one(request, venta_id):
    template_path = 'venta/reporte_one.html'
    today = timezone.now()
    todayD = str(timezone.now().day) + '-' + str(timezone.now().month) + '-' + str(timezone.now().year) 

    enc= FacturaHeader.objects.filter(id=venta_id).first()
    if enc:
        detalle = FacturaBody.objects.filter(factura__id=venta_id)
        sumaG = FacturaBody.objects.filter(factura__id=venta_id).aggregate(g=Sum('ganancias'))
    else:
        detalle = {}
    
    context = {
        'detalle':detalle,
        'enc':enc,
        'today':today,
        'gananciasT':sumaG,
        'request':request
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="venta({todayD}).pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def imprimir_rango(request, f1, f2):
    template_path = "venta/imprimir_rango.html"
    today = timezone.now()
    f1= parse_date(f1)
    f2= parse_date(f2)
    f2 = f2 + timedelta(days=1)

    enc = FacturaBody.objects.filter(factura__fecha__gte=f1, factura__fecha__lt=f2)
    f2 = f2 - timedelta(days=1)
    context = {
        'request': request,
        'f1': f1, 
        'f2': f2,
        'enc': enc,
        'today': today
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="venta_rango({f1} a {f2}).pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response