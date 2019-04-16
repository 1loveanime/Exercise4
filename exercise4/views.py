import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404


from .forms import RegistrationForm, PersonAddForm
from .models import PersonDetail




from django.views.generic import ListView


# def welcome(request):
# 	if request.user.is_authenticated:	
# 		person_list = PersonDetail.objects.filter(user=request.user).order_by('last_name')
# 		if 'export_info_csv' in request.GET:
# 			response = HttpResponse(content_type='text/csv')
# 			response['Content-Disposition'] = 'attachment; filename="person_list.csv"'
# 			writer = csv.writer(response)
# 			writer.writerow(["First Name", "Last Name", "Contact Number", "Address"])
# 			for field in person_list:
# 				writer.writerow([field.first_name, field.last_name, field.contact_number, field.address])
# 			return response
# 	else:
# 		person_list = PersonDetail.objects.none()
# 	return render(request, 'exercise4/welcome.html', {'person_list':person_list})


class Welcome(ListView):
	template_name = 'exercise4/welcome.html'
	model = PersonDetail
	context_object_name = 'person_list'

	def get(self, *args, **kwargs):
		if 'export_info_csv' in self.request.GET:
			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="person_list.csv"'
			writer = csv.writer(response)
			writer.writerow(["First Name", "Last Name", "Contact Number", "Address"])
			person_list = PersonDetail.objects.filter(user=self.request.user)
			for field in person_list:
				writer.writerow([field.first_name, field.last_name, field.contact_number, field.address])
			return response
		else:
			return super().get(request, *args, **kwargs)

	def get_queryset(self):
			self.request.user.is_authenticated
			person_list = PersonDetail.objects.filter(user=self.request.user).order_by('last_name')
			return person_list


def registration(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
	else:
		form = RegistrationForm()
	return render(request, 'registration/registration.html', {'form':form})


@login_required
def person_add(request):
	if request.method == 'POST':
		form = PersonAddForm(request.POST, request.FILES)
		if form.is_valid():
			form = form.save(commit='False')
			form.user = request.user
			form.save()
			return redirect('welcome')
	else:
		form = PersonAddForm()
	return render(request, 'exercise4/person_add.html', {'form':form})


@login_required
def person_delete(request, pk):
	form = get_object_or_404(PersonDetail, pk=pk)
	if request.method == 'POST':
		form.delete()
		return redirect('welcome')
	return render(request, 'exercise4/person_delete_confirmation.html', {'form':form})


@login_required
def person_update(request, pk):
	person_data = get_object_or_404(PersonDetail, pk=pk)
	if request.method == 'POST':
		form = PersonAddForm(request.POST, request.FILES, instance=person_data)
		if form.is_valid():
			form = form.save(commit='False')
			form.user = request.user
			form.save()
			return redirect('welcome')
	else:
		form = PersonAddForm(instance=person_data)
	return render(request, 'exercise4/person_add.html', {'form':form})


@login_required
def person_import(request):
	if request.method == 'POST':
		csv_file = request.FILES['csv_file']
		if not csv_file.name.endswith('.csv'):
			messages.error(request,'File is not CSV type')
			return redirect('person_import')
		file_data = csv_file.read().decode("utf-8")
		lines = file_data.split("\n")
		print(lines)
		for line in lines:				
			fields = line.split(",")
			data_dict = {}
			data_dict["first_name"] = fields[0]
			data_dict["last_name"] = fields[1]
			data_dict["contact_number"] = fields[2]
			data_dict["address"] = fields[3]
			form = PersonAddForm(data_dict)
			if form.is_valid():
				form = form.save(commit='False')
				form.user = request.user
				form.save()
			else:
				messages.error(request, "Invalid Information detected, uploading of data halted.")
				redirect('person_import')
				break
		return redirect('welcome')
	return render(request, 'exercise4/person_import.html')