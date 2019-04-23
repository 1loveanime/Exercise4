from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView
from tablib import Dataset

from .forms import RegistrationForm, PersonAddForm
from .models import PersonDetail
from .resources import PersonResource


@method_decorator(login_required, name='dispatch')
class Welcome(ListView):
	template_name = 'exercise4/welcome.html'
	model = PersonDetail
	context_object_name = 'person_list'

	def get(self, request, *args, **kwargs):
		if 'export_info_csv' in self.request.GET:
			person_resource = PersonResource()
			queryset = PersonDetail.objects.filter(user=self.request.user)
			dataset = person_resource.export(queryset)
			response = HttpResponse(dataset.csv, content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="persons.csv"'
			return response
		else:
			return super().get(request, *args, **kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			person_list = PersonDetail.objects.filter(user=self.request.user).order_by('last_name')
			return person_list


class Registration(CreateView):
	template_name = 'registration/registration.html'
	form_class = RegistrationForm
	success_url = '/accounts/login/'

	def form_valid(self, form):
		form.save()
		return super().form_valid(form)


class PersonSaveMixin(object):

	def form_valid(self, form):
		form_modify = form.save(commit=False)
		form_modify.user = self.request.user
		form_modify.save()
		return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class PersonAdd(PersonSaveMixin, CreateView):
	template_name = 'exercise4/person_add.html'
	form_class = PersonAddForm
	success_url = '/'


@method_decorator(login_required, name='dispatch')
class PersonDelete(DeleteView):
	template_name = 'exercise4/person_delete_confirmation.html'
	success_url = '/'
	context_object_name = 'person_data'

	def get_object(self):
		person_data = get_object_or_404(PersonDetail, pk=self.kwargs.get('pk'))
		return person_data


@method_decorator(login_required, name='dispatch')
class PersonUpdate(PersonSaveMixin, UpdateView):
	template_name = 'exercise4/person_add.html'
	form_class = PersonAddForm
	success_url = '/'

	def get_object(self):
		person_data = get_object_or_404(PersonDetail, pk=self.kwargs.get('pk'))
		return person_data


@method_decorator(login_required, name='dispatch')
class PersonImport(TemplateView):
	template_name = 'exercise4/person_import.html'

	def post(self, request):
		person_resource = PersonResource()
		dataset = Dataset()
		new_persons = self.request.FILES['csv_file']

		if not new_persons.name.endswith('.csv'):
			messages.error(self.request, "The uploaded file is not a CSV file format.")
			return super().get(request)
		try:
			imported_data = dataset.load(new_persons.read().decode('utf-8'),format='csv')
		except:
			messages.error(self.request, "There is a problem on your CSV File. Please check the Headers."
				"Please use only FirstName, LastName, ContactNo and Address.")
			return redirect('/person/import')

		result = person_resource.import_data(dataset, dry_run=True)

		if result.has_errors():
			messages.error(self.request, "The uploaded file has errors on it, please double check it.")
		else:
			person_resource.import_data(dataset, dry_run=False)
			messages.success(self.request, "Successfully uploaded the CSV file!")

		return redirect('/person/import')