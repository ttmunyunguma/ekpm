from django.forms import ModelForm

from manager.models import LandLord


class LandLordForm(ModelForm):
    class Meta:
        model = LandLord
        exclude = ['managed_by', 'date_created']


