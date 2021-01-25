from django.urls import path

from . import views_member

urlpatterns = [
  path('createMember', views_member.create_member, name='Create Order'),
]