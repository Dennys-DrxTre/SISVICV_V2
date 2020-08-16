from django.urls import path, re_path
from .reportes import reportventa_all, reportmascota_all,\
    reportproducto_all, reportclient_one, reportmascot_one, reportcliente_all
from .views import ReportePersonasPDF


urlpatterns = [
    path('ventaall/', reportventa_all, name='ventaall'),
    path('mascotaall/', reportmascota_all, name='mascotaall'),
    path('productoall/', reportproducto_all, name='productoall'),
    path('cliente/one/<int:cedula>', reportclient_one, name='clienteone'),
    path('mascota/one/<int:id>', reportmascot_one, name='mascotaone'),
    path('clienteall/', reportcliente_all, name='clientall'),


    path('allclient/', ReportePersonasPDF.as_view(), name='reportclient')
]