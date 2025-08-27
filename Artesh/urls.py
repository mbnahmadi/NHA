"""
URL configuration for Artesh project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from Station.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/dates",get_dates),
    path("api/stations",get_stations),
    path('api/images/', list_images, name='list_images'),
    path('api/images/<str:image_name>/', get_image, name='get_image'),
    path('api/categorized_images/', categorize_images, name='categorize_images'),
    #path('api/<str:date>/<str:nv_type>/<str:folder_pic>/<str:pic_name>/', show_image, name='show_image'),
    path("api/sounding/", soundingView),
    path("api/crosssection/",CrossSectionView),
    path("api/paramspic/",parametere_pic),



    #re_path(r'^api/(?P<date>\d+)/(?P<model>\w+)/(?P<params>\w+)/(?P<image>[^/]+)$', views.show_image),
]

