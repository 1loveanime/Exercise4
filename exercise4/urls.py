from django.urls import path

from . import views

urlpatterns = [
    path('', views.Welcome.as_view(), name='welcome'),
    path('accounts/register', views.registration, name='registration'),
    path('person/new', views.person_add, name='person_add'),
    path('person/<pk>/delete', views.person_delete, name='person_delete'),
    path('person/<pk>/update', views.person_update, name='person_update'),
    path('person/import', views.person_import, name='person_import'),
]