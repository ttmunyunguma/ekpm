from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView

from manager.forms import LandLordForm, PropertyForm, PropertyUnitForm, PremiseForm
from manager.models import LandLord, PropertyManager, Property, PropertyUnit, Premise


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class PortalHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/index.html'


class LandLordCreateView(LoginRequiredMixin, CreateView):
    form_class = LandLordForm
    template_name = 'manager/landlords_create.html'

    def form_valid(self, form):
        form.instance.managed_by = PropertyManager.objects.get(
            user=self.request.user
        ).organisation
        return super(LandLordCreateView, self).form_valid(form)


class LandLordListView(LoginRequiredMixin, ListView):
    model = LandLord
    paginate_by = 10
    template_name = 'manager/landlords_list.html'

    def get_context_data(self, **kwargs):
        context = super(LandLordListView, self).get_context_data(**kwargs)
        landlords = LandLord.objects.filter(
            managed_by=PropertyManager.objects.get(
                user=self.request.user).organisation,
            is_active=True
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


class LandLordDetailView(LoginRequiredMixin, DetailView):
    model = LandLord
    context_object_name = 'landlord'
    template_name = 'manager/landlords_detail.html'


class LandLordUpdateView(LoginRequiredMixin, UpdateView):
    form_class = LandLordForm
    template_name = 'manager/landlords_create.html'
    model = LandLord


class PropertyCreateView(LoginRequiredMixin, CreateView):
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


class PropertyListView(LoginRequiredMixin, ListView):
    model = Property
    paginate_by = 10
    template_name = 'manager/property_list.html'

    def get_context_data(self, **kwargs):
        context = super(PropertyListView, self).get_context_data(**kwargs)
        properties = Property.objects.filter(
            organisation_managing=PropertyManager.objects.get(
                user=self.request.user).organisation,
            is_active=True
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


class PropertyDetailView(LoginRequiredMixin, DetailView):
    model = Property
    context_object_name = 'property'
    template_name = 'manager/property_detail.html'


class PropertyUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PropertyForm
    template_name = 'manager/property_create.html'
    model = Property

    def get_form_kwargs(self):
        kwargs = super(PropertyUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class PropertyUnitListView(LoginRequiredMixin, ListView):
    model = PropertyUnit
    paginate_by = 10
    template_name = 'manager/property_unit_list.html'
    context_object_name = 'units'

    def get_queryset(self, *args, **kwargs):
        query = super(PropertyUnitListView, self).get_queryset().filter(
            property_id=self.kwargs.get('prop'),
            is_active=True
        ).order_by('id')
        self.request.session['prop'] = self.kwargs.get('prop')
        return query

    def get_context_data(self, **kwargs):
        context = super(PropertyUnitListView, self).get_context_data(**kwargs)
        context['prop'] = self.kwargs.get('prop')
        context['property'] = Property.objects.get(id=self.kwargs.get('prop'))
        return context


class PropertyUnitCreateView(LoginRequiredMixin, CreateView):
    form_class = PropertyUnitForm
    template_name = 'manager/property_unit_create.html'

    def form_valid(self, form, **kwargs):
        form.instance.property = Property.objects.get(id=self.kwargs.get('prop'))
        return super(PropertyUnitCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PropertyUnitCreateView, self).get_context_data(**kwargs)
        context['prop'] = self.request.session.get('prop')
        return context


class PropertyUnitDetailView(LoginRequiredMixin, DetailView):
    model = PropertyUnit
    context_object_name = 'unit'
    template_name = 'manager/property_unit_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PropertyUnitDetailView, self).get_context_data(**kwargs)
        context['prop'] = self.request.session.get('prop')
        return context


class PropertyUnitUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PropertyUnitForm
    template_name = 'manager/property_unit_create.html'
    model = PropertyUnit

    def get_context_data(self, **kwargs):
        context = super(PropertyUnitUpdateView, self).get_context_data(**kwargs)
        context['prop'] = self.request.session.get('prop')
        return context


class PropertyPremiseListView(LoginRequiredMixin, ListView):
    model = Premise
    paginate_by = 10
    template_name = 'manager/premise_list.html'
    context_object_name = 'premises'

    def get_queryset(self, *args, **kwargs):
        query = super(PropertyPremiseListView, self).get_queryset().filter(
            property_id=self.kwargs.get('prop'),
            is_active=True
        ).order_by('id')
        self.request.session['prop'] = self.kwargs.get('prop')
        return query

    def get_context_data(self, **kwargs):
        context = super(PropertyPremiseListView, self).get_context_data(**kwargs)
        context['prop'] = self.kwargs.get('prop')
        context['property'] = Property.objects.get(id=self.kwargs.get('prop'))
        return context


class PropertyPremiseCreateView(LoginRequiredMixin, CreateView):
    form_class = PremiseForm
    template_name = 'manager/premise_create.html'

    def form_valid(self, form, **kwargs):
        form.instance.property = Property.objects.get(id=self.kwargs.get('prop'))
        return super(PropertyPremiseCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PropertyPremiseCreateView, self).get_context_data(**kwargs)
        context['prop'] = self.request.session.get('prop')
        return context


class PropertyPremiseDetailView(LoginRequiredMixin, DetailView):
    model = Premise
    context_object_name = 'premise'
    template_name = 'manager/premise_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PropertyPremiseDetailView, self).get_context_data(**kwargs)
        context['prop'] = self.request.session.get('prop')
        return context


class PropertyPremiseUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PremiseForm
    template_name = 'manager/premise_create.html'
    model = Premise

    def get_context_data(self, **kwargs):
        context = super(PropertyPremiseUpdateView, self).get_context_data(**kwargs)
        context['prop'] = self.request.session.get('prop')
        return context

