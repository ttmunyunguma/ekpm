from django.urls import path
from . import views

app_name = 'manager'

urlpatterns = [
    path('', views.PortalHomeView.as_view(), name='portal'),
    path('landlords/', views.LandLordListView.as_view(), name='landlords'),
    path('landlords/new/', views.LandLordCreateView.as_view(), name='landlords_new'),

]
