from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView

from manager.forms import LandLordForm
from manager.models import LandLord, PropertyManager


class PortalHomeView(TemplateView):
    template_name = 'manager/index.html'


class LandLordCreateView(CreateView):
    form_class = LandLordForm
    template_name = 'manager/landlords_create.html'
    success_url = reverse_lazy('manager:landlords')

    def form_valid(self, form):
        form.instance.managed_by = PropertyManager.objects.get(
            user=self.request.user
        ).organisation
        return super(LandLordCreateView, self).form_valid(form)


class LandLordListView(ListView):
    model = LandLord
    paginate_by = 10
    template_name = 'manager/landlords_list.html'

    def get_context_data(self, **kwargs):
        context = super(LandLordListView, self).get_context_data(**kwargs)
        landlords = LandLord.objects.filter(
            managed_by=PropertyManager.objects.get(
                user=self.request.user).organisation
        )
        paginator = Paginator(landlords, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)

        context['landlords'] = pages
        return context
