from django import forms
from geopy.exc import GeocoderServiceError
from geopy.geocoders import Nominatim, ArcGIS
from manager.models import LandLord, Property, PropertyManager, PropertyUnit, Premise


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

    land_lord = forms.ModelChoiceField(label='Land Lord*', queryset=None, widget=forms.Select(
        attrs={'class': 'ui-selectonemenu ui-widget ui-state-default ui-corner-all'}), required=True)
    first_erected_date = forms.DateField(label='First Erected Date',
                                         widget=forms.SelectDateWidget(years=range(1900, 2100)), required=False)
    property_acquired_date = forms.DateField(label='Property Acquired Date',
                                             widget=forms.SelectDateWidget(years=range(1900, 2100)), required=False)
    management_started_date = forms.DateField(label='Management Started Date',
                                              widget=forms.SelectDateWidget(years=range(1900, 2100)), required=False)
    management_stopped_date = forms.DateField(label='Management Stopped Date',
                                              widget=forms.SelectDateWidget(years=range(1900, 2100)), required=False)
    property_disposed_date = forms.DateField(label='Property Disposed Date',
                                             widget=forms.SelectDateWidget(years=range(1900, 2100)), required=False)
    title = forms.CharField(
        label='Property Title*', widget=forms.TextInput(
            attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all'}))
    property_value = forms.DecimalField(
        max_digits=15, decimal_places=2, initial=0.00, label='Property Value($)',
        widget=forms.NumberInput(
            attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all', }))
    address = forms.CharField(
        label='Address*',
        widget=forms.TextInput(attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all'}))
    city = forms.CharField(
        label='City*',
        widget=forms.TextInput(attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all'}))
    description = forms.CharField(
        label='Property Description',
        widget=forms.Textarea(
            attrs={'class': 'ui-inputfield ui-inputtextarea ui-widget ui-state-default ui-corner-all'}))
    lot_size = forms.DecimalField(
        label='Lot Size(sqmts)',
        max_digits=15, decimal_places=3, initial=0.000,
        widget=forms.NumberInput(
            attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all', }))
    building_size = forms.DecimalField(
        label='Building Size(sqmts)',
        max_digits=15, decimal_places=3, initial=0.000,
        widget=forms.NumberInput(
            attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all', }))
    acquisition_cost = forms.DecimalField(
        label='Acquisition Cost($)',
        max_digits=15, decimal_places=2, initial=0.00,
        widget=forms.NumberInput(
            attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all', }))
    selling_price = forms.DecimalField(
        label='Selling Price($)',
        max_digits=15, decimal_places=2, initial=0.00,
        widget=forms.NumberInput(attrs={
            'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all'}))
    zone = forms.CharField(
        label='Property Zone',
        widget=forms.TextInput(attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all'}),
        required=False)
    details = forms.CharField(
        label='Extra Details',
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
            print("**************GeoCode success***************")
        except GeocoderServiceError:
            property_obj.geographic_location = (address + " " + city + " " + country.name)
            print("**************GeoCode failed***************")
        if commit:
            property_obj.save()

        return property_obj


class PropertyUnitForm(forms.ModelForm):
    unit_title = forms.CharField(
        label='Unit Title*',
        widget=forms.TextInput(attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all'}))
    total_area = forms.DecimalField(
        label='Total Area(sqmts)*',
        max_digits=15, decimal_places=3, initial=0.000,
        widget=forms.NumberInput(
            attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all'}))
    details = forms.CharField(
        label='Unit Details',
        widget=forms.Textarea(
            attrs={'class': 'ui-inputfield ui-inputtextarea ui-widget ui-state-default ui-corner-all'}), required=False)

    class Meta:
        model = PropertyUnit
        exclude = ['property', 'date_created', 'last_updated', 'is_active']


class PremiseForm(forms.ModelForm):
    premise_title = forms.CharField(
        label='Premise Title*',
        widget=forms.TextInput(attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all'}))
    total_area = forms.DecimalField(
        label='Total Area(sqmts)*',
        max_digits=15, decimal_places=3, initial=0.000,
        widget=forms.NumberInput(
            attrs={'class': 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all'}))
    details = forms.CharField(
        label='Unit Details',
        widget=forms.Textarea(
            attrs={'class': 'ui-inputfield ui-inputtextarea ui-widget ui-state-default ui-corner-all'}), required=False)

    class Meta:
        model = Premise
        exclude = ['property', 'date_created', 'last_updated', 'is_active']

