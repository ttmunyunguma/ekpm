from django.urls import path
from . import views

app_name = 'manager'

urlpatterns = [
    path('', views.PortalHomeView.as_view(), name='portal'),
    path('landlords/', views.LandLordListView.as_view(), name='landlords'),
    path('landlords/new/', views.LandLordCreateView.as_view(), name='landlords_new'),
    path('landlords/<int:pk>/', views.LandLordDetailView.as_view(), name='landlord_detail'),
    path('landlords/update/<int:pk>/', views.LandLordUpdateView.as_view(), name='landlord_update'),

    path('properties/', views.PropertyListView.as_view(), name='properties'),
    path('properties/new/', views.PropertyCreateView.as_view(), name='properties_new'),
    path('properties/<int:pk>/', views.PropertyDetailView.as_view(), name='property_detail'),
    path('properties/update/<int:pk>/', views.PropertyUpdateView.as_view(), name='property_update'),

]
