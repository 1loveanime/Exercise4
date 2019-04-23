from django.urls import path

from . import views

urlpatterns = [
    path('', views.Welcome.as_view(), name='welcome'),
    path('accounts/register', views.Registration.as_view(), name='registration'),
    path('person/new', views.PersonAdd.as_view(), name='person_add'),
    path('person/<pk>/delete', views.PersonDelete.as_view(), name='person_delete'),
    path('person/<pk>/update', views.PersonUpdate.as_view(), name='person_update'),
    path('person/import', views.PersonImport.as_view(), name='person_import'),
]