from django.urls import path
from . import views

app_name = 'manager'

urlpatterns = [
    # LandLords
    path('', views.PortalHomeView.as_view(), name='portal'),
    path('landlords/', views.LandLordListView.as_view(), name='landlords'),
    path('landlords/new/', views.LandLordCreateView.as_view(), name='landlords_new'),
    path('landlords/<int:pk>/', views.LandLordDetailView.as_view(), name='landlord_detail'),
    path('landlords/<int:pk>/update/', views.LandLordUpdateView.as_view(), name='landlord_update'),
    # Properties
    path('properties/', views.PropertyListView.as_view(), name='properties'),
    path('properties/new/', views.PropertyCreateView.as_view(), name='properties_new'),
    path('properties/<int:pk>/', views.PropertyDetailView.as_view(), name='property_detail'),
    path('properties/<int:pk>/update/', views.PropertyUpdateView.as_view(), name='property_update'),
    # Property Units
    path('properties/<int:prop>/units/', views.PropertyUnitListView.as_view(), name='property_units'),
    path('properties/<int:prop>/units/new/', views.PropertyUnitCreateView.as_view(), name='property_units_new'),
    path('properties/<int:prop>/units/<int:pk>/', views.PropertyUnitDetailView.as_view(), name='property_units_detail'),
    path('properties/<int:prop>/units/<int:pk>/update/', views.PropertyUnitUpdateView.as_view(),
         name='property_units_update'),
    # Premises
    path('properties/<int:prop>/premises/', views.PropertyPremiseListView.as_view(), name='property_premises'),
    path('properties/<int:prop>/premises/new/', views.PropertyPremiseCreateView.as_view(),
         name='property_premises_new'),
    path('properties/<int:prop>/premises/<int:pk>/', views.PropertyPremiseDetailView.as_view(),
         name='property_premises_detail'),
    path('properties/<int:prop>/premises/<int:pk>/update/', views.PropertyPremiseUpdateView.as_view(),
         name='property_premises_update'),
    # Tenants
    path('tenants/', views.AllTenantsListView.as_view(), name='tenants'),
    path('properties/<int:prop>/tenants/', views.TenantListView.as_view(), name='property_tenants'),
    path('properties/<int:prop>/tenants/new/', views.TenantCreateView.as_view(), name='property_tenant_new'),
    path('properties/<int:prop>/tenants/<int:pk>/', views.TenantDetailView.as_view(), name='property_tenant_detail'),
    path('properties/<int:prop>/tenants/<int:pk>/update/', views.TenantUpdateView.as_view(),
         name='property_tenant_update'),

    # Lease
    path('properties/<int:prop>/tenants/<int:ten>/lease/new/', views.LeaseCreateView.as_view(),
         name='tenants_lease_new'),
    path('properties/<int:prop>/tenants/<int:ten>/lease/<int:pk>/', views.LeaseDetailView.as_view(),
         name='tenant_lease_detail'),
    path('properties/<int:prop>/tenants/<int:ten>/lease/<int:pk>/update/', views.LeaseUpdateView.as_view(),
         name='tenant_lease_update'),

]
