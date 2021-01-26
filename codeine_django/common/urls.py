from django.urls import path

from . import views_member
from . import views_content_provider

urlpatterns = [
  path('createMember', views_member.create_member, name='Create Member'),
  path('contentProviders', views_content_provider.content_provider_view, name='Create content provider, get all content providers'),
  path('contentProviders/<slug:pk>', views_content_provider.protected_content_provider_view, name='Get content provider, activate or deactivate content provider')
]