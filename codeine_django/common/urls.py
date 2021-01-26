from django.urls import path

from . import views_member
from . import views_content_provider

urlpatterns = [
  path('createMember', views_member.create_member, name='Create Member'),
  path('/contentProvider/create', views_content_provider.create_content_provider, name='Create Content Provider'),
  path('/contentProvider/all', views_content_provider.get_all_content_providers, name='Get all Content Providers'),
  path('/contentProvider/<slug:pk>', views_content_provider.protected_content_provider_view, name='View Content Provider')
  path('/contentProvider/<slug:pk>/activate', views_content_provider.activate_content_provider, name='Activate Content Provider')
  path('/contentProvider/<slug:pk>/deactivate', views_content_provider.deactivate_content_provider, name='Deactivate Content Provider')
]