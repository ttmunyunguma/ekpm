from django import forms
from geopy.exc import GeocoderServiceError
from geopy.geocoders import Nominatim, ArcGIS
from manager.models import LandLord, Property, PropertyManager, PropertyUnit, Premise, Tenant, Lease
from django.utils.translation import ugettext_lazy as _

text_input_style = 'ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all'
text_area_style = 'ui-inputfield ui-inputtextarea ui-widget ui-state-default ui-corner-all'
select_one_menu_style = 'ui-selectonemenu ui-widget ui-state-default ui-corner-all'


class LandLordForm(forms.ModelForm):
    class Meta:
        model = LandLord
        exclude = ['managed_by', 'date_created', 'last_updated', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': text_input_style}),
            'phone': forms.TextInput(attrs={'class': text_input_style}),
            'address': forms.TextInput(attrs={'class': text_input_style}),
            'city': forms.TextInput(attrs={'class': text_input_style}),
            'identification': forms.TextInput(attrs={'class': text_input_style}),
            'bank': forms.TextInput(attrs={'class': text_input_style}),
            'bank_branch': forms.TextInput(attrs={'class': text_input_style}),
            'bank_account_number': forms.TextInput(attrs={'class': text_input_style}),
            'details': forms.Textarea(attrs={'class': text_area_style}),
            'representative': forms.TextInput(attrs={'class': text_input_style}),
        }


class PropertyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PropertyForm, self).__init__(*args, **kwargs)
        self.fields['land_lord'].queryset = LandLord.objects.filter(
            managed_by=PropertyManager.objects.get(
                user=user
            ).organisation
        )

    class Meta:
        model = Property
        exclude = ['organisation_managing', 'geographic_location', 'date_created', 'last_updated', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': text_input_style}),
            'land_lord': forms.Select(attrs={'class': select_one_menu_style}),
            'first_erected_date': forms.SelectDateWidget(years=range(1900, 2100)),
            'property_acquired_date': forms.SelectDateWidget(years=range(1900, 2100)),
            'management_started_date': forms.SelectDateWidget(years=range(1900, 2100)),
            'management_stopped_date': forms.SelectDateWidget(years=range(1900, 2100)),
            'property_disposed_date': forms.SelectDateWidget(years=range(1900, 2100)),
            'property_value': forms.NumberInput(attrs={'class': text_input_style}),
            'address': forms.TextInput(attrs={'class': text_input_style}),
            'city': forms.TextInput(attrs={'class': text_input_style}),
            'description': forms.Textarea(attrs={'class': text_area_style}),
            'lot_size': forms.NumberInput(attrs={'class': text_input_style}),
            'building_size': forms.NumberInput(attrs={'class': text_input_style}),
            'acquisition_cost': forms.NumberInput(attrs={'class': text_input_style}),
            'selling_price': forms.NumberInput(attrs={'class': text_input_style}),
            'zone': forms.TextInput(attrs={'class': text_input_style}),
            'details': forms.Textarea(attrs={'class': text_area_style}),
        }
        labels = {
            'property_value': _('Property Value ($)'),
            'description': _('Property Description'),
            'lot_size': _('Lot Size (sqmts)'),
            'building_size': _('Building Size (sqmts)'),
            'acquisition_cost': _('Acquisition Cost($)'),
            'selling_price': _('Selling Price ($)'),
            'zone': _('Property Zone'),
            'details': _('Extra Details'),
        }

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
    class Meta:
        model = PropertyUnit
        exclude = ['property', 'date_created', 'last_updated', 'is_active']
        widgets = {
            'unit_title': forms.TextInput(attrs={'class': text_input_style}),
            'total_area': forms.NumberInput(attrs={'class': text_input_style}),
            'details': forms.Textarea(attrs={'class': text_area_style}),
        }
        labels = {
            'total_area': _('Total Area (sqmts)*'),
        }


class PremiseForm(forms.ModelForm):
    class Meta:
        model = Premise
        exclude = ['property', 'date_created', 'last_updated', 'is_active']
        labels = {
            'total_area': _('Total Area (sqmts)'),
        }
        widgets = {
            'premise_title': forms.TextInput(attrs={'class': text_input_style}),
            'total_area': forms.NumberInput(attrs={'class': text_input_style}),
            'details': forms.Textarea(attrs={'class': text_area_style})
        }


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
            'tenant_representative': forms.TextInput(attrs={'class': text_input_style}),
            'tenant_representative_capacity': forms.TextInput(attrs={'class': text_input_style}),
            'owner_representative': forms.TextInput(attrs={'class': text_input_style}),
            'owner_representative_capacity': forms.TextInput(attrs={'class': text_input_style}),
            'rent_review_notes': forms.Textarea(attrs={'class': text_area_style}),
            'monthly_rent_amount': forms.NumberInput(attrs={'class': text_input_style}),
            'monthly_rate': forms.NumberInput(attrs={'class': text_input_style}),
            'escalation_percentage': forms.NumberInput(attrs={'class': text_input_style}),
            'recovery_percentage': forms.NumberInput(attrs={'class': text_input_style}),
            'monthly_recovery_amount': forms.NumberInput(attrs={'class': text_input_style}),
            'recovery_notes': forms.Textarea(attrs={'class': text_area_style}),
            'cash_deposit_amount': forms.NumberInput(attrs={'class': text_input_style}),
            'bank_guarantee_amount': forms.NumberInput(attrs={'class': text_input_style}),
            'deposit_notes': forms.Textarea(attrs={'class': text_area_style}),
            'lease_documentation_fee': forms.NumberInput(attrs={'class': text_input_style}),
            'late_payment_interest_percentage': forms.NumberInput(attrs={'class': text_input_style}),
        }
        labels = {
            'monthly_rent_amount': _('Monthly Rent Amount ($)'),
            'monthly_rate': _('Monthly Rate (%)'),
            'escalation_percentage': _('Escalation (%)'),
            'recovery_percentage': _('Recoveries (%)'),
            'monthly_recovery_amount': _('Monthly Recovery Amount ($)'),
            'cash_deposit_amount': _('Cash Deposit Amount ($)'),
            'bank_guarantee_amount': _('Bank Guarantee Amount ($)'),
            'lease_documentation_fee': _('Lease Documentation Fee ($)'),
            'late_payment_interest_percentage': _('Late Payment Interest (%)'),

        }
