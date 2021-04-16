from django.urls import path

from . import views_ide

urlpatterns = [
    # members views
    path('', views_ide.init_ide, name='Init an IDE'),
    path('/<slug:port_number>', views_ide.check_ide_status_view, name='Checks IDE status'),
]
