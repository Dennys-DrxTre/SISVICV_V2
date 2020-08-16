from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime
from django.db.models import Sum
from django.http import HttpResponse
from django.contrib.auth import authenticate

from apps.inicio.views import SinPermiso

from apps.venta.models import FacturaHeader, FacturaBody
from apps.inv.models import Producto
from apps.regmedic.models import Cliente

from .forms import VentaEncForm

# MODULOS PARA EL DJANGO RESTFRAMEWORK

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import ProductoSerializers
from django.db.models import Q

# Create your views here.

class VentaView(SinPermiso, generic.ListView):
    model = FacturaBody
    template_name= 'venta/Venta_list.html'
    context_object_name = 'obj'
    permission_required = "venta.view_facturabody"
    



# VISTAS DE LAS VENTAS
@login_required(login_url='/login/')
@permission_required('venta.add_facturaheader', login_url= 'inicio:accesodene')
def Factura(request, id=None):
    if not request.user.is_authenticated:
        return redirect ("login")
    else:
        template_name = "venta/facturacion.html"

        detalles = {}
        cliente = Cliente.objects.all()

        if request.method == 'GET':
            enc = FacturaHeader.objects.filter(pk=id).first()
            if not enc:
                encabezado = {
                    'id': 0,
                    'fecha':datetime.today(),
                    'cliente': 0,
                    'sub_total': 0.00,
                    'descuento': 0.00,
                    'total': 0.00
                }
                detalles = None
            else:
                encabezado = {
                    'id': enc.id,
                    'fecha': enc.fecha,
                    'cliente': enc.cliente,
                    'sub_total': enc.sub_total,
                    'descuento': enc.descuento,
                    'total': enc.total
                }
                detalles = FacturaBody.objects.filter(factura=enc)

            contexto = {'enc': encabezado, 'body': detalles, 'cliente': cliente}

        if request.method == 'POST':
            cliente = request.POST.get("enc_cliente")
            fecha = request.POST.get("fecha")
            cli = Cliente.objects.get(pk=cliente)

            if not id:
                enc = FacturaHeader(cliente= cli, fecha = fecha)

                if enc:
                    enc.save()
                    id = enc.id
            else:
                enc = FacturaHeader.objects.filter(pk=id).first()
                if enc:
                    enc.cliente = cli
                    enc.save()
            if not id:
                messages.error("No se pudo identificar el Nro. de Factura")
                return redirect('venta:Venta_list')

            codigo = request.POST.get("codigo")
            cantidad =  request.POST.get("cantidad")
            precioVenta = request.POST.get("precioVenta")
            sub_total =  request.POST.get("sub_total_detalle")
            descuento =  request.POST.get("descuento_detalle")
            total =  request.POST.get("total")


            prod = Producto.objects.get(codigo=codigo)
            Ganancias = float(float(prod.ganancia) * float(int(cantidad)) - float(descuento))

            body = FacturaBody(
                factura= enc,
                producto=prod, 
                cantidad=cantidad, 
                precio=precioVenta, 
                sub_total=sub_total, 
                descuento=descuento, 
                total=total,
                ganancias=Ganancias
                )

            if body:
                body.save()
            
            return redirect("venta:factura_editar", id=id )

        return render(request, template_name, contexto)

class ProductoView(LoginRequiredMixin, generic.ListView):
    model = Producto
    template_name = "venta/buscar_producto.html"
    permission_required = "inv.view_producto"    


# BORRAR UNA FACTURA
@login_required(login_url='/login/')
@permission_required('venta.delete_facturaheader', login_url= 'inicio:accesodene')
def borrar_factura(request, id):
    template_name = "venta/factura_borrar_detalle.html"
    body = FacturaBody.objects.get(pk=id)

    if request.method == "GET":
        contexto = {'body':body}
    
    if request.method == "POST":
        usr = request.POST.get("user")
        pas = request.POST.get("pass")

        user = authenticate(username=usr, password=pas)

        if not user:
            return HttpResponse("Usuario o contraseña incorrecta")
        if not user.is_active:
            return HttpResponse("Usuario inactivo")

        if user.is_staff:
            body.id = None
            body.cantidad = (-1 * body.cantidad)
            body.sub_total = (-1 * body.sub_total)
            body.descuento = (-1 * body.descuento)
            body.total = (-1 * body.total)
            body.producto.stock = (body.producto.stock + body.cantidad)
            body.save()

            return HttpResponse("ok")

        return HttpResponse("Usuario no autorizado")
        
    return render(request, template_name, contexto)

# VISTAS DE DJANGO RESTFRAMEWORK

class ProductoList(APIView):
    def get(self, request):
        prod = Producto.objects.all()
        data = ProductoSerializers(prod, many=True).data
        return Response(data)

class ProductoDetalle(APIView):
    def get(self, request, codigo):
        prod = get_object_or_404(Producto, Q(codigo=codigo))
        data = ProductoSerializers(prod).data
        return Response(data)