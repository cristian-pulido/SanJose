"""SanJose URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, include
from django.contrib.auth import views
from django.views.generic import TemplateView
from django.contrib.auth.views import logout

from .views import error, crearingreso, crearradiologia, crearuci, crearneurologia, crearbold, crearinformante, \
    crearseguimiento, crearradiologiaf, crearmoca, crearnps, crearneuropsi, visionimagen, validarmovimiento, alinear, crearlectura

from .views import reportes, run_pipeline

urlpatterns = [
    path('', lambda x: HttpResponseRedirect('/login')),
    path('admin/', admin.site.urls),
    path('carga/', include('apps.fileupload.urls')),
    path('paciente/', include('apps.paciente.urls')),
    path('validacion/', include('apps.validacion.urls')),
    path('graficas/',include('apps.graphs.urls')),

    url(r'^login/$', views.login, name='login'),
    url(r'^accounts/logout/$', logout, {'template_name': 'registration/logout.html'},name='logout'),
    url(r'^login-error$', error, name='login-error'),
    path('report_builder/', include('report_builder.urls')),
    path('script/creari/<int:pk>/', crearingreso, name='crear_ingreso'),
    path('script/crearr/<int:pk>/', crearradiologia, name='crear_radiologia'),
    path('script/crearu/<int:pk>/', crearuci, name='crear_uci'),
    path('script/crearn/<int:pk>/', crearneurologia, name='crear_neurologia'),
    path('script/crearb/<int:pk>/', crearbold, name='crear_bold'),
    path('script/crearinf/<int:pk>/', crearinformante, name='crear_informante'),
    path('script/crears/<int:pk>/', crearseguimiento, name='crear_seguimiento'),
    path('script/crearrf/<int:pk>/<slug:razon>/', crearradiologiaf, name='crear_rf'),
    path('script/crearnps/<int:pk>/<slug:razon>/<slug:fecha>/', crearnps, name='crear_nps'),
    path('script/crearm/<int:pk>/', crearmoca, name='crear_moca'),
    path('script/crearnpsi/<int:pk>/', crearneuropsi, name='crear_neuropsi'),
    path('script/crearl/<int:pk>/<slug:tipo>/', crearlectura, name='crear_lectura'),
    path('script/filtros_img/<slug:pk>/', visionimagen, name='vision_img'),
    path('script/vmovimiento/<slug:tipo>/<int:pk>/<slug:v1>/<slug:v2>/', validarmovimiento, name='v_movimiento'),
    path('script/alinear/<slug:tipo>/<int:pk>/<slug:img>/<slug:der>/<slug:frente>/<slug:arriba>/<slug:x>/<slug:y>/<slug:z>/<slug:tx>/<slug:ty>/<slug:tz>/<slug:save>/', alinear, name='alinear'),

  
    url(r'^reportes$',reportes,name="reportes"),

    url(r'^visualizador', TemplateView.as_view(template_name='slicedrop/index.html'), name="visor"),

    url(r'^accounts/', include('allauth.urls')),
    
    path('procesamiento/', include('apps.procesamiento.urls')),
    
    path('script/run_pipeline/<int:user_pk>/<int:img_pk>/<int:pipeline_pk>/', run_pipeline, name='run_pipeline'),




]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


