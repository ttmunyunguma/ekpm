from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView


class LandingPage(TemplateView):
    template_name = 'index.html'

