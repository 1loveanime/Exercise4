from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db import models


class PersonDetail(models.Model):
	first_name = models.CharField(max_length=40)
	last_name = models.CharField(max_length=40)
	phone_regex = RegexValidator(regex=r'^\+639\d{9}$',
		message="Phone number must be entered in the format: \"+639XXXXXXXXX\". (x represents a number)")
	contact_number = models.CharField(validators=[phone_regex], max_length=13)
	address = models.CharField(max_length=100, null=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	profilepicture = models.ImageField(upload_to='gallery', default='gallery/default.png', null=True, blank=True)

	def __str__(self):
		return self.first_name + " " + self.last_name

	# def save(self):