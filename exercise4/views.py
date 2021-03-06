from braces.views import AjaxResponseMixin, JsonRequestResponseMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView, ListView, TemplateView, View
from tablib import Dataset

from .forms import RegistrationForm, PersonAddForm
from .models import PersonDetail
from .resources import PersonResource


class Registration(CreateView):
	template_name = 'registration/registration.html'
	form_class = RegistrationForm
	success_url = '/accounts/login/'

	def form_valid(self, form):
		form.save()
		return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class WelcomeView(FormView, ListView):
	template_name = 'exercise4/welcome.html'
	model = PersonDetail
	context_object_name = 'person_list'
	form_class = PersonAddForm
	paginate_by = 10

	def get(self, request, *args, **kwargs):
		if 'export_info_csv' in self.request.GET:
			person_resource = PersonResource()
			queryset = self.get_queryset()
			dataset = person_resource.export(queryset)
			response = HttpResponse(dataset.csv, content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="personslist.csv"'
			return response
		else:
			return super().get(request, *args, **kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			person_list = PersonDetail.objects.filter(user=self.request.user).order_by('first_name')
			return person_list


@method_decorator(login_required, name='dispatch')
class PersonUpdateAjaxView(AjaxResponseMixin, JsonRequestResponseMixin, View):
	def post_ajax(self, request, *args, **kwargs):
		person_instance = None
		data_pk = request.POST.get("data_pk", None)

		if data_pk:
			if PersonDetail.objects.filter(pk=data_pk).exists():
				person_instance = PersonDetail.objects.get(pk=data_pk)

		if person_instance:
			person_add_form = PersonAddForm(data=self.request.POST, instance=person_instance)
		else:
			person_add_form = PersonAddForm(data=self.request.POST)

		if person_add_form.is_valid():
			form_modify = person_add_form.save(commit=False)
			form_modify.user = self.request.user
			form_modify.save()
			return self.render_json_response({
				'status': "OK",
				'pk': form_modify.pk,
				'first_name': form_modify.first_name,
				'last_name': form_modify.last_name,
				'contact_number': form_modify.contact_number,
				'address': form_modify.address,
				'profilepicture': form_modify.profilepicture.url,
				'is_update': bool(person_instance),
				'is_success': True,
			})
		else:
			error_dict = person_add_form.errors.as_json()
			return self.render_json_response({
				'status': "OK",
				'message': error_dict
			})


@method_decorator(login_required, name='dispatch')
class PersonDeleteAjaxView(AjaxResponseMixin, JsonRequestResponseMixin, View):

		def post_ajax(self, request, *args, **kwargs):
			data_pk = request.POST.get('data_pk', None)

			if data_pk:
				PersonDetail.objects.filter(pk=data_pk).delete()
				return self.render_json_response({
				'status': "OK",
				'pk': data_pk,

				})
			else:
				return self.render_json_response({
				'status': "OK",
				})


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