import request

from import_export import resources, fields
from .models import PersonDetail

# pip install django-threadlocals-0.10
from threadlocals.threadlocals import get_current_request

class PersonResource(resources.ModelResource):
	first_name = fields.Field(attribute='first_name', column_name='FirstName')
	last_name = fields.Field(attribute='last_name', column_name='LastName')
	contact_number = fields.Field(attribute='contact_number', column_name='ContactNo')
	address = fields.Field(attribute='address', column_name='Address')
	user = fields.Field(attribute='user', column_name='user')

	def get_instance(self, instance_loader, row): #EFFING RESEARCH WHAT THIS DOES, THIS UNREQUIRES THE ID FIELD ON CSV BUT I DUNO HOW OR WHY
		return False

	# def after_import_instance(self, instance, new, **kwargs):
	# 	print ('------------------')
	# 	print (self)
	# 	print(instance)
	# 	print(new)
	# 	print(kwargs)
	# 	address = 'addressbiktima'

	# def after_import_row(self, row, row_result, **kwargs):
	# 	# row.update({user:'mehehehehe'})
	# 	print(row)
	# 	print('\n\n\n')



	def before_save_instance(self, instance, using_transactions, dry_run):
		# instance.user = self.request.user
		request = get_current_request()
		# print ("=================================================")
		# print(request.user)
		instance.user = request.user

	class Meta:
		model = PersonDetail
		fields = ('first_name', 'last_name', 'contact_number', 'address')
		# exclude = ('id', )
		# import_id_fields = ['id', ]