from django.shortcuts import redirect, render, get_object_or_404, reverse
from .models import Agent, Lead, Category
from django.views import generic
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm, StudentCreateModelForm
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganizerAndLoginRequiredMixin
from django.urls import reverse_lazy
# Create your views here.

# CRUD - Create, Retrieve, Update and Delete + List

class SignupView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm
    model = Lead
    def get_success_url(self):
        return reverse('login')

class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'

class LeadList(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/lead_list.html'
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user

        #Initial queryset of the entire organization
        if user.is_organizer:
            queryset = Lead.objects.filter(organisation=user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organisation=self.request.user.agent.organisation, agent__isnull=False)
            #Filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset
    
    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        if user.is_organizer:
            context['unassigned_leads'] = Lead.objects.filter(
                organisation=user.userprofile,
                agent__isnull=True,
            )
        return context

class LeadDetail(LoginRequiredMixin, generic.DetailView):
    template_name = 'leads/lead_detail.html'
    model = Lead
    def get_queryset(self):
        user = self.request.user

        #Initial queryset of the entire organization
        if user.is_organizer:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=self.request.user.agent.organisation)
            #Filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

class LeadCreate(OrganizerAndLoginRequiredMixin, generic.CreateView):
    model = Lead
    form_class = LeadModelForm
    template_name = 'leads/lead_create.html'
    def get_success_url(self):
        return reverse('leads:list')
    
    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()

        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )

        return redirect(self.get_success_url())

    #def form_valid(self, form):
        #lead = form.save(commit=False)
        #lead.organisation = self.request.user.userprofile
        #lead.save()

        #send_mail(
            #subject="A lead has been created",
            #message="Go to the site to see the new lead",
            #from_email="test@test.com",
            #recipient_list=["test2@test.com"]
        #)

        #return redirect(self.get_success_url())
    

def lead_create(request):
    form = LeadModelForm()
    if request.method == 'POST':
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leads:list')
    context = {
        "form": form
    }
    return render(request, 'leads/lead_create.html', context)

class LeadUpdate(OrganizerAndLoginRequiredMixin, generic.UpdateView):
    model = Lead
    form_class = LeadModelForm
    template_name = 'leads/lead_update.html'

    def get_queryset(self):
        user = self.request.user
        #Initial queryset of leads for the entire organization
        return Lead.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse('leads:list')

def lead_update(request, pk):
    lead = get_object_or_404(Lead, id=pk)
    if request.method == 'POST':
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('leads:list')
    else:
        form = LeadModelForm(instance=lead)
    context = {
        'lead': lead,
        'form': form
    }
    return render(request, 'leads/lead_update.html', context)

class LeadDelete(LoginRequiredMixin, generic.DeleteView):
    template_name = 'leads/lead_delete.html'
    model = Lead
    def get_success_url(self):
        return reverse('leads:list')
        
    def get_queryset(self):
        user = self.request.user
        #Initial queryset of leads for the entire organization
        return Lead.objects.filter(organisation=user.userprofile)


def lead_delete(request, pk):
    lead = get_object_or_404(Lead, id=pk)
    lead.delete()
    return redirect('leads:list')

def lead_update(request, pk):
    lead = get_object_or_404(Lead, id=pk)
    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']

            lead.first_name = first_name
            lead.last_name = last_name
            lead.age = age
            lead.save()
            return redirect('leads:list')
    else:
        form = LeadForm(initial={
            'first_name': lead.first_name,
            'last_name': lead.last_name,
            'age': lead.age
        })
    context = {
        'lead': lead,
        'form': form
    }
    return render(request, 'leads/lead_update.html', context)

def create_lead(request):
     form = LeadModelForm()
     if request.method == 'POST':
         form = LeadModelForm(request.POST)
         if form.is_valid():
             print('The form is valid')
             print(form.cleaned_data)
             first_name = form.cleaned_data['first_name']
             last_name = form.cleaned_data['last_name']
             age = form.cleaned_data['age']
             agent = form.cleaned_data['agent']
             Lead.objects.create(
                 first_name=first_name,
                 last_name=last_name,
                 age=age,
                 agent=agent
             )
             print('Lead has been created')
             return redirect('leads:list')
     context = {
         "form": form
     }
     return render(request, 'leads/lead_create.html', context)

class AssignAgentView(OrganizerAndLoginRequiredMixin, generic.FormView):
    template_name = 'leads/assign_agent.html'
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update  ({
            'request': self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse('leads:list')

    def form_valid(self, form):
        agent = form.cleaned_data['agent']
        lead = Lead.objects.get(id=self.kwargs['pk'])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/category_list.html'
    context_object_name = 'category_list'

    def get_context_data(self, **kwargs):
        user = self.request.user

        context = super().get_context_data(**kwargs)
        if user.is_organizer:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=self.request.user.agent.organisation)
        
        context.update({
        "unassigned_lead_count": Lead.objects.filter(category__isnull=True).count()
        })
        return context
    def get_queryset(self):
        user = self.request.user

        #Initial queryset of the entire organization
        if user.is_organizer:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=self.request.user.agent.organisation)
        return queryset

class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'leads/category_detail.html'
    context_object_name = 'category'

    #def get_context_data(self, **kwargs):
    #    user = self.request.user
    #    context = super(CategoryDetailView, self).get_context_data(**kwargs)
    #    qs = Lead.objects.filter(category=self.get_object())
    #    leads = self.get_object().leads.all()
    #    context.update({
    #        'leads': leads
    #    })
    #    return context

    def get_queryset(self):
        user = self.request.user

        #Initial queryset of the entire organization
        if user.is_organizer:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=self.request.user.agent.organisation)
        return queryset

class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Lead
    form_class = LeadCategoryUpdateForm
    template_name = 'leads/lead-category-update.html'

    def get_queryset(self):
        user = self.request.user

        #Initial queryset of the entire organization
        if user.is_organizer:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=self.request.user.agent.organisation)
            #Filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse('leads:detail', kwargs={'pk': self.get_object().id})

class LeadCreateView(generic.CreateView):
    model = Lead
    form_class = StudentCreateModelForm
    template_name = 'leads/second-create.html'
    success_url = reverse_lazy('landing-page')