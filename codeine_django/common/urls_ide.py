from django.urls import path

from . import views_ide

urlpatterns = [
    # members views
    path('', views_ide.init_ide, name='Init an IDE'),
]
