from django.urls import path

from . import views

urlpatterns = [
    path('', views.WelcomeView.as_view(), name='welcome'),
    path('accounts/register', views.Registration.as_view(), name='registration'),
    path('person/import', views.PersonImport.as_view(), name='person_import'),
    path('ajax/person/delete', views.PersonDeleteAjaxView.as_view(), name='ajax_person_delete'),
    path('ajax/person/update', views.PersonUpdateAjaxView.as_view(), name='ajax_person_update'),
]