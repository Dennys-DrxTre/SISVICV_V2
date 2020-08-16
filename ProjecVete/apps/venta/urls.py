from django.urls import path

from .views import VentaView, ProductoList, ProductoDetalle, Factura, ProductoView, borrar_factura

from .reportes import reportes_all, reporte_one, imprimir_rango
urlpatterns = [

    path('Reporte/Listado', reportes_all, name='Ventas_Reporte'),
    path('Reporte/One/<int:venta_id>', reporte_one, name='Venta_Reporte'),
    path('imprimir-rango/<str:f1>/<str:f2>', imprimir_rango, name='reporte_rango'),

    # PATH DEL DJANGO RESTFRAMEWORK
    path('v1/productos/', ProductoList.as_view(), name='lista'),
    path('v1/productos/<str:codigo>/', ProductoDetalle.as_view(), name='detalle'),

    # PATH DE LAS VENTAS
    path('', VentaView.as_view(), name='Venta_list'),
    path('factura/nueva/', Factura, name = 'factura'),
    path('factura/editar/<int:id>', Factura, name = 'factura_editar'),
    # PATH DE LA VENTANA MODAL CON LOS PRODUCTOS
    path('producto/list/', ProductoView.as_view(), name='lista_popup'),
    # BORRAR UNA VENTA DE LA FACTURA
    path('factura/borrar-detalle/<int:id>', borrar_factura, name='factura_borrar'),

]

    
    
