from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required

from apps.regmedic.models import Cliente, Mascota, Consulta, Despa, Vacuna
from apps.regmedic .forms import ClienteForm, MascotaForm
from apps.venta.models import FacturaHeader, FacturaBody
from apps.inv.models import Producto

from django.db.models import Avg
from django.db.models import Sum

from django.db.models.functions import TruncMonth, ExtractMonth, Coalesce
from django.db.models import Count
from django.utils.timezone import datetime

# Create your views here.

class SinPermiso(PermissionRequiredMixin, LoginRequiredMixin):
    login_url = 'inicio:login'
    raise_exception=False
    redirect_field_name="redirect_to"

    def handle_no_permission(self):
        from django.contrib.auth.models import AnonymousUser
        if not self.request.user==AnonymousUser():
            self.login_url = 'inicio:accesodene'
        return HttpResponseRedirect(reverse_lazy(self.login_url))

class FechaHora():
    Hoy = datetime.today()

@login_required(login_url='/login/')
@permission_required('regmedic.view_cliente', login_url= 'inicio:accesodene')
def Inicio(request):
    template_name='inicio/inicio.html'
    suma = FacturaBody.objects.filter().aggregate(Sum('ganancias'))

    producto = Producto.objects.filter(estado=True)
    contMascota = Mascota.objects.filter(estado=True)
    
    fecha = FacturaBody.objects.annotate(month=TruncMonth('factura__fecha')).values('month').annotate(ganancias=Sum('ganancias'))
    # Los 5 ultimos movimientos
    clientes = Cliente.objects.all().order_by('-updated')
    mascotas = Mascota.objects.all().order_by('-id')
    ventas = FacturaBody.objects.all().order_by('-id')

    context= {
        'total': suma, 
        'fecha': fecha, 
        'cliente': clientes, 
        'mascota':mascotas, 
        'venta': ventas,
        'prod':producto,
        'contmascot':contMascota
        }

    return render(request, template_name, context)


@login_required(login_url='/login/')
@permission_required('regmedic.view_cliente', login_url= 'inicio:accesodene')
def Estadisticas(request):
    template_name = 'inicio/Estadisticas.html'
#DONUT CHART PRODUCTOS CON MENOS STOCK
    labelsP = []
    dataP = []
    Productos = Producto.objects.all().order_by('-stock')[:8]

    for prod in Productos:
        labelsP.append(prod.nombre)
        dataP.append(prod.stock)
#LINE CHART GANANCIAS MENSUALES
    ventas = FacturaBody.objects.annotate(month=TruncMonth('factura__fecha')).values('month').annotate(ganancias=Sum('ganancias'))
    if len(ventas) < (12):
        ventas = FacturaBody.objects.annotate(month=TruncMonth('factura__fecha')).values('month').annotate(ganancias=Sum('ganancias'))
    else:
        result1 = len(ventas) - int(12)
        ventas = FacturaBody.objects.annotate(month=TruncMonth('factura__fecha')).values('month').annotate(ganancias=Sum('ganancias'))[result1:]
#BAR CHART CANTIDAD DE VENTAS MENSUALES
    cantidad = FacturaHeader.objects.annotate(month=TruncMonth('fecha')).values('month').annotate(cantidad=Count('id'))
    if len(cantidad) < (12):
        cantidad = FacturaHeader.objects.annotate(month=TruncMonth('fecha')).values('month').annotate(cantidad=Count('id'))
        print(cantidad)
    else: 
        result2 = len(cantidad) - int(12)
        cantidad = FacturaHeader.objects.annotate(month=TruncMonth('fecha')).values('month').annotate(cantidad=Count('id'))[result2:]
        print(cantidad)

#DONUT CHART CANTIDAD TOTAL DE CONSULTAS, VACUNACIONES Y DESPARASITACIONES
    consulta = Consulta.objects.aggregate(Count('id'))
    desparasitacion = Despa.objects.aggregate(Count('id'))
    vacunacion = Vacuna.objects.aggregate(Count('id'))

    context = {
        'labels':labelsP,
        'data':dataP, 
        'ventas':ventas, 
        'cantidad':cantidad,
        'c':consulta,
        'v':vacunacion,
        'd':desparasitacion
    }
    return render(request, template_name, context )

class AccesoDene(LoginRequiredMixin, generic.TemplateView):
    template_name= 'inicio/sin_privilegios.html'
    login_url='inicio:login'

# VIEWS DE MANTENIMIENTO

# CLIENTES
class Manten_Client(SinPermiso, generic.ListView):
    model = Cliente
    template_name = "inicio/Manten_Cliente.html"
    permission_required = "admin.view_entry"    

    
class Manten_Client_edit(SinPermiso, generic.UpdateView):
    model = Cliente
    context_object_name = "obj"
    form_class = ClienteForm
    template_name = "inicio/Manten_Cliente_Edit.html"
    success_url = reverse_lazy('inicio:man_client')
    permission_required = "admin.edit_entry"

# MASCOTAS
class Manten_Pets(SinPermiso, generic.ListView):
    model = Mascota
    template_name = "inicio/Manten_Pets.html"
    permission_required = "admin.view_entry"    

class Manten_Pets_edit(SinPermiso, generic.UpdateView):
    template_name = "inicio/Manten_Pets_Edit.html"
    model = Mascota
    context_object_name = "obj"
    form_class = MascotaForm
    success_url = reverse_lazy('inicio:man_pets')
    permission_required = "admin.edit_entry"


#PRODUCTOS
class ProductoMlist(SinPermiso, generic.ListView):
    model= Producto
    template_name="inicio/ProductoM_list.html"
    context_object_name = "obj"
    permission_required = "admin.view_entry"   

class ProductoMDel(SinPermiso, generic.DeleteView):
    model = Producto
    template_name = 'inicio/ProductoM_del.html' 
    success_url = reverse_lazy('inicio:list_prod')
    success_message = "Producto Eliminado Correctamente"
    context_object_name = "obj"
    permission_required = "admin.delete_entry"   


# EMPLEADOS
class empleadosList(SinPermiso, generic.ListView):
    model = User
    template_name = "inicio/NuevoEmpleado.html"
    permission_required = "admin.view_entry"    


class EmpleadosDelete(SinPermiso, generic.DeleteView):
    model = User
    template_name = "inicio/DeleteEmpleado.html"
    success_url = reverse_lazy('inicio:list_emp')
    context_object_name = "obj"
    permission_required = "admin.delete_entry"
