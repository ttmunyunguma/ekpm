from django import forms

from manager.models import LandLord, Property, PropertyManager


class LandLordForm(forms.ModelForm):
    class Meta:
        model = LandLord
        exclude = ['managed_by', 'date_created', 'last_updated', 'is_active']


class PropertyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PropertyForm, self).__init__(*args, **kwargs)
        self.fields['land_lord'].queryset = LandLord.objects.filter(
            managed_by=PropertyManager.objects.get(
                user=user
            ).organisation
        )

    land_lord = forms.ModelChoiceField(queryset=None, widget=forms.Select, required=True)
    first_erected_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2100)), required=False)
    property_acquired_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2100)), required=False)
    management_started_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2100)), required=False)
    management_stopped_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2100)), required=False)
    property_disposed_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2100)), required=False)

    class Meta:
        model = Property
        exclude = ['organisation_managing', 'date_created', 'last_updated', 'is_active']

