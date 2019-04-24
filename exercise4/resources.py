from threadlocals.threadlocals import get_current_request

from import_export import resources, fields
from .models import PersonDetail


class PersonResource(resources.ModelResource):
	first_name = fields.Field(attribute='first_name', column_name='FirstName')
	last_name = fields.Field(attribute='last_name', column_name='LastName')
	contact_number = fields.Field(attribute='contact_number', column_name='ContactNo')
	address = fields.Field(attribute='address', column_name='Address')

	def get_instance(self, instance_loader, row): #EFFING RESEARCH WHAT THIS DOES, THIS UNREQUIRES THE ID FIELD ON CSV BUT I DUNO HOW OR WHY
		return False

	def before_save_instance(self, instance, using_transactions, dry_run):
		request = get_current_request()
		instance.user = request.user

	class Meta:
		model = PersonDetail
		fields = ('first_name', 'last_name', 'contact_number', 'address')