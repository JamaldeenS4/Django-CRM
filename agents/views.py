from django.shortcuts import render, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganizerAndLoginRequiredMixin
import random
from django.core.mail import send_mail
# Create your views here.


class AgentList(OrganizerAndLoginRequiredMixin, generic.ListView):
    template_name = 'agents/agent_list.html'
    context_object_name = 'agents'
    
    def get_queryset(self):
        request_user_userprofile = self.request.user.userprofile
        return Agent.objects.filter(organisation=request_user_userprofile)

class AgentCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    template_name = 'agents/agent_create.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organizer = False
        user.set_password(f"{random.randint(0,1000000)}")
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile
        )
        send_mail(
            subject='You are invited to be an agent',
            message='You were added as an agent in DJ CRM. Please login to start working',
            from_email='admin@test.com',
            recipient_list=[user.email]
        )
        #agent.organisation = self.request.user.userprofile
        #agent.save()
        return super(AgentCreateView, self).form_valid(form)

class AgentDetailView(OrganizerAndLoginRequiredMixin, generic.DetailView):
    template_name = 'agents/agent_detail.html'
    context_object_name = 'agent'

    def get_queryset(self):
        request_user_userprofile = self.request.user.userprofile
        return Agent.objects.filter(organisation=request_user_userprofile)

class AgentUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'agents/agent_update.html'
    form_class = AgentModelForm
    context_object_name = 'agent'

    def get_success_url(self):
        return reverse('agents:list')

    def get_queryset(self):
        request_user_userprofile = self.request.user.userprofile
        return Agent.objects.filter(organisation=request_user_userprofile)

class AgentDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'agents/agent_delete.html'
    context_object_name = 'agent'

    def get_queryset(self):
        request_user_userprofile = self.request.user.userprofile
        return Agent.objects.filter(organisation=request_user_userprofile)

    def get_success_url(self):
        return reverse('agents:list')