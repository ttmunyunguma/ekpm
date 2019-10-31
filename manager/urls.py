from django.urls import path
from . import views

app_name = 'manager'

urlpatterns = [
    path('', views.PortalHomeView.as_view(), name='portal'),

]
