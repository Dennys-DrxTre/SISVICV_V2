from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from apps.inicio.views import SinPermiso
from .models import Departamento, Categoria, Producto
from .forms import DeparatamentoForm, CategoriaForm, ProductoForm
from django.http import HttpResponse
import json
from django.http import JsonResponse

# Create your views here.

# SECCION DE DEPARTAMENTO / ALMACEN

class DepartamentoView(SinPermiso, generic.ListView):
    model= Departamento
    template_name="inv/Departamento_list.html"
    context_object_name = "obj"
    permission_required = "inv.view_departamento"    

class DepartamentoNew(SuccessMessageMixin, SinPermiso, generic.CreateView):
    model = Departamento
    template_name = 'inv/Departamento_form.html'
    context_object_name = "obj"
    form_class = DeparatamentoForm
    success_url = reverse_lazy('inv:Departamento_list')
    success_message = 'Almacén Agregado Correctamente'
    permission_required = "inv.add_departamento"    

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class DepartamentoEdit(SuccessMessageMixin, SinPermiso, generic.UpdateView):
    model = Departamento
    template_name = 'inv/Departamento_form.html'
    context_object_name = "obj"
    form_class = DeparatamentoForm
    success_url = reverse_lazy('inv:Departamento_list')
    success_message = 'Almacén Actualizado Correctamente'
    permission_required = "inv.change_departamento"    


    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

@login_required(login_url='/login/')
@permission_required('inv.change_departamento', login_url= 'inicio:accesodene')
def DepartaInact(request, id):
    departamento = Departamento.objects.filter(pk=id).first()
    contexto={}
    template_name = 'inv/Departamento_del.html'

    if not departamento:
        return redirect('inv:Departamento_list')
    
    if request.method=='GET':
        contexto={'obj':departamento}
    
    if request.method=='POST':
        if departamento.estado ==True:
            departamento.estado=False
            departamento.save()
            messages.success(request, 'Almacén Desactivado Correctamente')

        else:
            departamento.estado=True
            departamento.save()
            messages.success(request, 'Almacén Activado Correctamente')

        return redirect('inv:Departamento_list')

    return render(request,template_name,contexto)
    

# SECCION DE CATEGORIAS

class CategoriaView(SinPermiso, generic.ListView):
    model= Categoria
    template_name="inv/Categoria_list.html"
    context_object_name = "obj"
    permission_required = "inv.view_categoria"    


class CategoriaNew(SuccessMessageMixin, SinPermiso, generic.CreateView):
    model = Categoria
    template_name = 'inv/Categoria_form.html'
    context_object_name = "obj"
    form_class = CategoriaForm
    success_url = reverse_lazy('inv:Categoria_list')
    success_message = 'Categoria Agregado Correctamente'
    permission_required = "inv.add_categoria"    



    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class CategoriaEdit(SuccessMessageMixin , SinPermiso, generic.UpdateView):
    model = Categoria
    template_name = 'inv/Categoria_form.html'
    context_object_name = "obj"
    form_class = CategoriaForm
    success_url = reverse_lazy('inv:Categoria_list')
    success_message = 'Categoria Actualizado Correctamente'
    permission_required = "inv.change_categoria"    


    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

@login_required(login_url='/login/')
@permission_required('inv.change_categoria', login_url= 'inicio:accesodene')
def CategoriaInact(request, id):
    categoria = Categoria.objects.filter(pk=id).first()
    contexto={}
    template_name = 'inv/Categoria_del.html'

    if not categoria:
        return redirect('inv:Categoria_list')
    
    if request.method=='GET':
        contexto={'obj':categoria}
    
    if request.method=='POST':
        if categoria.estado ==True:
            categoria.estado=False
            categoria.save()
            messages.success(request, 'Categoria Desactivada Correctamente')

        else:
            categoria.estado=True
            categoria.save()
            messages.success(request, 'Categoria Activada Correctamente')

        return redirect('inv:Categoria_list')

    return render(request,template_name,contexto)

# SECCION PRODUCTO

class ProductoView(SinPermiso, generic.ListView):
    model= Producto
    template_name="inv/Producto_list.html"
    context_object_name = "obj"
    permission_required = "inv.view_producto"    
 

class ProductoNew(SuccessMessageMixin , SinPermiso, generic.CreateView):
    model = Producto
    template_name = 'inv/Producto_form.html'
    context_object_name = "obj"
    form_class = ProductoForm
    success_url = reverse_lazy('inv:Producto_list')
    success_message = 'Producto Agregado Correctamente'
    permission_required = "inv.add_producto"    

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

class ProductoEdit(SuccessMessageMixin , SinPermiso, generic.UpdateView):
    model = Producto
    template_name = 'inv/Producto_form.html'
    context_object_name = "obj"
    form_class = ProductoForm
    success_url = reverse_lazy('inv:Producto_list')
    success_message = 'Producto Actualizado Correctamente'
    permission_required = "inv.change_producto"    

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

@login_required(login_url='/login/')
@permission_required('inv.change_producto', login_url= 'inicio:accesodene')
def ProductoInact(request, id):
    producto = Producto.objects.filter(pk=id).first()
    contexto={}
    template_name = 'inv/Producto_del.html'


    if not producto:
        return redirect('inv:Categoria_list')
    
    if request.method=='GET':
        contexto={'obj':producto}
    
    if request.method=='POST':
        if producto.estado ==True:
            producto.estado=False
            producto.save()
            messages.success(request, 'Producto Desactivado Correctamente')
        else:
            producto.estado=True
            producto.save()
            messages.success(request, 'Producto Activado Correctamente')

        return redirect('inv:Producto_list')

    return render(request,template_name,contexto)

@login_required(login_url='/login/')
@permission_required('inv.change_producto', login_url= 'inicio:accesodene')
def producto_add(request, id):
    producto = Producto.objects.filter(id=id).first()
    template_name = 'inv/Producto_add_more.html'
    contexto={}

    if request.method=='GET':
        contexto={
            'obj':producto,
        }

    if request.method=='POST':
        #Obtenemos los valores del POST 
        mas = request.POST.get("more")
        venta = request.POST.get("venta")
        compra = request.POST.get("compra")
        #Agregamos a la base de datos
        producto.stock = (producto.stock + float(mas))
        producto.precioCompra = float(compra)
        producto.precioVenta = float(venta)
        producto.save()

        return redirect('inv:Producto_list')
    return render(request, template_name, contexto)
    