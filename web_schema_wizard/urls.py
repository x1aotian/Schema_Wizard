"""web_schema_wizard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('main/', views.main, name='main'),  # three params illustrated in: https://docs.djangoproject.com/en/4.0/intro/tutorial01/
    path('<int:id>/view2', views.view2 , name = 'view2'),
    path('original_view/', views.original_view, name = 'original_view'),
    path('choose_type/', views.choose_type, name = 'choose_type'),
    path('choose_type_mod_loop/', views.choose_type_mod_loop, name = 'choose_type_mod_loop')
]
