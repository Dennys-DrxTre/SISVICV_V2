"""ProjecVete URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('apps.inicio.urls', 'inicio'), namespace='inicio')),
    path('inv/', include(('apps.inv.urls', 'inv'), namespace='inv')),
    path('regMedic/',include(('apps.regmedic.urls', 'regmedic'), namespace='regmedic')),
    path('ventas/',include(('apps.venta.urls', 'venta'), namespace='venta')),
    path('accounts/', include('apps.registration.urls' )),
    path('reporte/', include(('apps.reporte.urls', 'reporte'), namespace='reporte')),


    path('accounts/', include('apps.registration.urls' )),
    path('accounts/', include('django.contrib.auth.urls')),

]
