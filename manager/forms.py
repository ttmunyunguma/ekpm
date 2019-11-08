from django import forms
from geopy.exc import GeocoderServiceError
from geopy.geocoders import Nominatim, ArcGIS
from manager.models import LandLord, Property, PropertyManager, PropertyUnit


class LandLordForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all'}))
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all'}))
    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all'}))
    city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all'}))
    identification = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all'}))
    bank = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all'}))
    bank_branch = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all'}))
    bank_account_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all'}))
    details = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'ui-inputfield ui-inputtextarea ui-widget ui-state-default ui-corner-all'}), required=False)
    representative = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all'}), required=False)

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

    land_lord = forms.ModelChoiceField(queryset=None, widget=forms.Select(
        attrs={'class': 'ui-selectonemenu ui-widget ui-state-default ui-corner-all'}), required=True)
    first_erected_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2100)), required=False)
    property_acquired_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2100)), required=False)
    management_started_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2100)), required=False)
    management_stopped_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2100)), required=False)
    property_disposed_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2100)), required=False)
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all'}))
    property_value = forms.DecimalField(
        widget=forms.TextInput(attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all',
                                      'placeholder': '0.00'}), required=False)
    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all'}))
    city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all'}))
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'ui-inputfield ui-inputtextarea ui-widget ui-state-default ui-corner-all'}))
    lot_size = forms.DecimalField(
        widget=forms.TextInput(attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all',
                                      'placeholder': '0.00'}), required=False)
    building_size = forms.DecimalField(
        widget=forms.TextInput(attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all',
                                      'placeholder': '0.00'}), required=False)
    acquisition_cost = forms.DecimalField(
        widget=forms.TextInput(attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all',
                                      'placeholder': '0.00'}), required=False)
    selling_price = forms.DecimalField(
        widget=forms.TextInput(attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all',
                                      'placeholder': '0.00'}), required=False)
    zone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all'}),
        required=False)
    details = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'ui-inputfield ui-inputtextarea ui-widget ui-state-default ui-corner-all'}), required=False)

    class Meta:
        model = Property
        exclude = ['organisation_managing', 'geographic_location', 'date_created', 'last_updated', 'is_active']

    def save(self, commit=True):
        property_obj = super(PropertyForm, self).save(commit=False)
        geolocator = ArcGIS(user_agent="eKPM")
        address = self.cleaned_data['address']
        city = self.cleaned_data['city']
        country = self.cleaned_data['country']
        try:
            property_obj.geographic_location = geolocator.geocode(address + " " + city + " " + country.name)
        except GeocoderServiceError:
            property_obj.geographic_location = (address + " " + city + " " + country.name)
            print(property_obj.geographic_location)
        if commit:
            property_obj.save()

        return property_obj


class PropertyUnitForm(forms.ModelForm):
    class Meta:
        model = PropertyUnit
        exclude = ['property', 'date_created', 'last_updated', 'is_active']
