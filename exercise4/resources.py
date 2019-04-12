from import_export import resources
from .models import PersonDetail

class PersonResource(resources.ModelResource):
   
   class Meta:
        model = PersonDetail
        exclude = ('user',)