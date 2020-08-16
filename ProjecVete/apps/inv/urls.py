from django.urls import path

from .views import DepartamentoView, DepartamentoNew, DepartamentoEdit, CategoriaView, CategoriaNew, CategoriaEdit, CategoriaInact, DepartaInact, ProductoView, ProductoNew, ProductoEdit, ProductoInact, producto_add

urlpatterns = [
#URLS DEPARTAMENTOS
    path('Departamentos/', DepartamentoView.as_view(), name='Departamento_list'),
    path('Departamento/new', DepartamentoNew.as_view(), name='Departamento_form'),
    path('Departamento/edit/<int:pk>', DepartamentoEdit.as_view(), name='Departamento_edit'),
    path('Departamento/inactivar/<int:id>', DepartaInact, name='Departamento_inac'),
#URLS CATEGORIAS
    path('Categorias/', CategoriaView.as_view(), name='Categoria_list'),
    path('Categoria/new', CategoriaNew.as_view(), name='Categoria_form'),
    path('Categoria/edit/<int:pk>', CategoriaEdit.as_view(), name='Categoria_edit'),
    path('Categoria/del/<int:id>', CategoriaInact, name='Categoria_inac'),
#URLS PRODUCTOS
    path('Productos/', ProductoView.as_view(), name='Producto_list'),
    path('Producto/new', ProductoNew.as_view(), name='Producto_form'),
    path('Producto/edit/<int:pk>', ProductoEdit.as_view(), name='Producto_edit'),
    path('Producto/del/<int:id>', ProductoInact, name='Producto_inac'),
    path('Producto/more/<int:id>', producto_add, name='producto_more'),
]