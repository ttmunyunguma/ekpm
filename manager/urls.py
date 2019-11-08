from django.urls import path
from . import views

app_name = 'manager'

urlpatterns = [
    path('', views.PortalHomeView.as_view(), name='portal'),
    path('landlords/', views.LandLordListView.as_view(), name='landlords'),
    path('landlords/new/', views.LandLordCreateView.as_view(), name='landlords_new'),
    path('landlords/<int:pk>/', views.LandLordDetailView.as_view(), name='landlord_detail'),
    path('landlords/<int:pk>/update/', views.LandLordUpdateView.as_view(), name='landlord_update'),

    path('properties/', views.PropertyListView.as_view(), name='properties'),
    path('properties/new/', views.PropertyCreateView.as_view(), name='properties_new'),
    path('properties/<int:pk>/', views.PropertyDetailView.as_view(), name='property_detail'),
    path('properties/<int:pk>/update/', views.PropertyUpdateView.as_view(), name='property_update'),

    path('properties/<int:prop>/units/', views.PropertyUnitListView.as_view(), name='property_units'),
    path('properties/<int:prop>/units/new/', views.PropertyUnitCreateView.as_view(), name='property_units_new'),
    path('properties/<int:prop>/units/<int:pk>/', views.PropertyUnitDetailView.as_view(), name='property_units_detail'),
    path('properties/<int:prop>/units/<int:pk>/update/', views.PropertyUnitUpdateView.as_view(),
         name='property_units_update'),

]
