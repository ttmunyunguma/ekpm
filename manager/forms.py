from django import forms
from geopy.exc import GeocoderServiceError
from geopy.geocoders import Nominatim, ArcGIS
from manager.models import LandLord, Property, PropertyManager, PropertyUnit, Premise, Tenant, Lease
from django.utils.translation import ugettext_lazy as _

text_input_style = 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all'
text_area_style = 'ui-inputfield ui-inputtextarea ui-widget ui-state-default ui-corner-all'


class LandLordForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': text_input_style}))
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': text_input_style}))
    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': text_input_style}))
    city = forms.CharField(
        widget=forms.TextInput(attrs={'class': text_input_style}))
    identification = forms.CharField(
        widget=forms.TextInput(attrs={'class': text_input_style}))
    bank = forms.CharField(
        widget=forms.TextInput(attrs={'class': text_input_style}))
    bank_branch = forms.CharField(
        widget=forms.TextInput(attrs={'class': text_input_style}))
    bank_account_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': text_input_style}))
    details = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': text_area_style}), required=False)
    representative = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': text_input_style}), required=False)

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
            attrs={'class': text_input_style}))
    property_value = forms.DecimalField(
        max_digits=15, decimal_places=2, initial=0.00, label='Property Value($)',
        widget=forms.NumberInput(
            attrs={'class': text_input_style, }))
    address = forms.CharField(
        label='Address*',
        widget=forms.TextInput(attrs={'class': text_input_style}))
    city = forms.CharField(
        label='City*',
        widget=forms.TextInput(attrs={'class': text_input_style}))
    description = forms.CharField(
        label='Property Description',
        widget=forms.Textarea(
            attrs={'class': text_area_style}))
    lot_size = forms.DecimalField(
        label='Lot Size(sqmts)',
        max_digits=15, decimal_places=3, initial=0.000,
        widget=forms.NumberInput(
            attrs={'class': text_input_style, }))
    building_size = forms.DecimalField(
        label='Building Size(sqmts)',
        max_digits=15, decimal_places=3, initial=0.000,
        widget=forms.NumberInput(
            attrs={'class': text_input_style, }))
    acquisition_cost = forms.DecimalField(
        label='Acquisition Cost($)',
        max_digits=15, decimal_places=2, initial=0.00,
        widget=forms.NumberInput(
            attrs={'class': text_input_style, }))
    selling_price = forms.DecimalField(
        label='Selling Price($)',
        max_digits=15, decimal_places=2, initial=0.00,
        widget=forms.NumberInput(attrs={
            'class': text_input_style}))
    zone = forms.CharField(
        label='Property Zone',
        widget=forms.TextInput(attrs={'class': text_input_style}),
        required=False)
    details = forms.CharField(
        label='Extra Details',
        widget=forms.Textarea(
            attrs={'class': text_area_style}), required=False)

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
        widget=forms.TextInput(attrs={'class': text_input_style}))
    total_area = forms.DecimalField(
        label='Total Area(sqmts)*',
        max_digits=15, decimal_places=3, initial=0.000,
        widget=forms.NumberInput(
            attrs={'class': text_input_style}))
    details = forms.CharField(
        label='Unit Details',
        widget=forms.Textarea(
            attrs={'class': text_area_style}), required=False)

    class Meta:
        model = PropertyUnit
        exclude = ['property', 'date_created', 'last_updated', 'is_active']


class PremiseForm(forms.ModelForm):
    premise_title = forms.CharField(
        label='Premise Title*',
        widget=forms.TextInput(attrs={'class': text_input_style}))
    total_area = forms.DecimalField(
        label='Total Area(sqmts)*',
        max_digits=15, decimal_places=3, initial=0.000,
        widget=forms.NumberInput(
            attrs={'class': text_input_style}))
    details = forms.CharField(
        label='Unit Details',
        widget=forms.Textarea(
            attrs={'class': text_area_style}), required=False)

    class Meta:
        model = Premise
        exclude = ['property', 'date_created', 'last_updated', 'is_active']


class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        exclude = ['property', 'date_created', 'last_updated', 'is_active', 'lease']
        labels = {
            'tenant_name': _('Tenant Name*'),
            'trading_as_list_name': _('Trading As / List Name*'),
            'identification_type': _('Identification Type*'),
            'identification': _('Identification Number*'),
            'email_1': _('Email*'),
            'email_2': _('Alternate Email'),
            'phone_1': _('Phone*'),
            'phone_2': _('Alternate Phone'),
            'postal_address': _('Postal Address*'),
            'domicile_address': _('Domicile Address'),
            'nationality': _('Nationality*'),
            'details': _('Extra Details'),
        }
        widgets = {
            'tenant_name': forms.TextInput(attrs={'class': text_input_style}),
            'trading_as_list_name': forms.TextInput(attrs={'class': text_input_style}),
            'identification': forms.TextInput(attrs={'class': text_input_style}),
            'email_1': forms.TextInput(attrs={'class': text_input_style, 'placeholder': _('your@email.com')}),
            'email_2': forms.TextInput(attrs={'class': text_input_style, 'placeholder': _('your@alt_email.com')}),
            'phone_1': forms.TextInput(attrs={'class': text_input_style}),
            'phone_2': forms.TextInput(attrs={'class': text_input_style}),
            'postal_address': forms.Textarea(attrs={'class': text_area_style}),
            'domicile_address': forms.Textarea(attrs={'class': text_area_style}),
            'details': forms.Textarea(attrs={'class': text_area_style}),
        }


class LeaseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        property_id = kwargs.pop('property')
        super(LeaseForm, self).__init__(*args, **kwargs)
        self.fields['premises'].queryset = Premise.objects.filter(property_id=property_id)
        self.fields['property_unit'].queryset = PropertyUnit.objects.filter(property_id=property_id)

    class Meta:
        model = Lease
        exclude = ['tenant_lessee', 'owner_lessor', 'organization_managing', 'created_by_manager',
                   'is_active', 'date_created', 'last_updated']

        widgets = {
            'lease_starts': forms.SelectDateWidget(years=range(2019, 2100)),
            'occupation_date': forms.SelectDateWidget(years=range(2019, 2100)),
            'lease_ends': forms.SelectDateWidget(years=range(1900, 2019)),
            'rent_review_date': forms.SelectDateWidget(years=range(2019, 2100)),
            'annual_rent_review_date': forms.SelectDateWidget(years=range(2019, 2100)),

        }



