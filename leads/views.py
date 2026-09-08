from django.shortcuts import redirect, render, get_object_or_404
from .models import Agent, Lead
from django.views import generic
from .forms import LeadForm, LeadModelForm
# Create your views here.

class LeadList(generic.ListView):
    template_name = 'leads/lead_list.html'
    context_object_name = 'leads'

    def get_queryset(self):
        return Lead.objects.all()

class LeadDetail(generic.DetailView):
    template_name = 'leads/lead_detail.html'
    model = Lead

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

def lead_delete(request, pk):
    lead = get_object_or_404(Lead, id=pk)
    lead.delete()
    return redirect('leads:list')





# def lead_update(request, pk):
#     lead = get_object_or_404(Lead, id=pk)
#     if request.method == "POST":
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']

#             lead.first_name = first_name
#             lead.last_name = last_name
#             lead.age = age
#             lead.save()
#             return redirect('leads:list')
#     else:
#         form = LeadForm(initial={
#             'first_name': lead.first_name,
#             'last_name': lead.last_name,
#             'age': lead.age
#         })
#     context = {
#         'lead': lead,
#         'form': form
#     }
#     return render(request, 'leads/lead_update.html', context)

# def create_lead(request):
#     form = LeadModelForm()
#     if request.method == 'POST':
#         form = LeadModelForm(request.POST)
#         if form.is_valid():
#             print('The form is valid')
#             print(form.cleaned_data)
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             agent = form.cleaned_data['agent']
#             Lead.objects.create(
#                 first_name=first_name,
#                 last_name=last_name,
#                 age=age,
#                 agent=agent
#             )
#             print('Lead has been created')
#             return redirect('leads:list')
#     context = {
#         "form": form
#     }
#     return render(request, 'leads/lead_create.html', context)