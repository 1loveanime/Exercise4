from import_export import resources, fields
from .models import PersonDetail

class PersonResource(resources.ModelResource):
   first_name = fields.Field(attribute='first_name', column_name='first_name')
   last_name = fields.Field(attribute='last_name', column_name='last_name')
   contact_number = fields.Field(attribute='contact_number', column_name='contact_number')
   address = fields.Field(attribute='address', column_name='address')

   def get_instance(self, instance_loader, row):
   		return False

   class Meta:
        model = PersonDetail
        fields = ('first_name', 'last_name', 'contact_number', 'address')
        export_order = fields
        # import_id_fields = ('id')

