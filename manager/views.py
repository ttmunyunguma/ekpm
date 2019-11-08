from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView

from manager.forms import LandLordForm, PropertyForm
from manager.models import LandLord, PropertyManager, Property


class PortalHomeView(TemplateView):
    template_name = 'manager/index.html'


class LandLordCreateView(CreateView):
    form_class = LandLordForm
    template_name = 'manager/landlords_create.html'

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


class LandLordDetailView(DetailView):
    model = LandLord
    context_object_name = 'landlord'
    template_name = 'manager/landlords_detail.html'


class LandLordUpdateView(UpdateView):
    form_class = LandLordForm
    template_name = 'manager/landlords_create.html'
    model = LandLord


class PropertyCreateView(CreateView):
    form_class = PropertyForm
    template_name = 'manager/property_create.html'

    def get_form_kwargs(self):
        kwargs = super(PropertyCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        form.instance.organisation_managing = PropertyManager.objects.get(
            user=self.request.user
        ).organisation
        return super(PropertyCreateView, self).form_valid(form)


class PropertyListView(ListView):
    model = Property
    paginate_by = 10
    template_name = 'manager/property_list.html'

    def get_context_data(self, **kwargs):
        context = super(PropertyListView, self).get_context_data(**kwargs)
        properties = Property.objects.filter(
            organisation_managing=PropertyManager.objects.get(
                user=self.request.user).organisation
        )
        paginator = Paginator(properties, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)

        context['properties'] = pages
        return context


class PropertyDetailView(DetailView):
    model = Property
    context_object_name = 'property'
    template_name = 'manager/property_detail.html'


class PropertyUpdateView(UpdateView):
    form_class = PropertyForm
    template_name = 'manager/property_create.html'
    model = Property

    def get_form_kwargs(self):
        kwargs = super(PropertyUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
