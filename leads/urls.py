from django.urls import path
from . import views

app_name ='leads'
urlpatterns = [
    path("", views.LeadList.as_view(), name='list'),
    path("<int:pk>/", views.LeadDetail.as_view(), name='detail'),
    path("create/", views.lead_create, name='create'),
    path("<int:pk>/update/", views.lead_update, name='update'),
    path("<int:pk>/delete/", views.lead_delete, name='delete')
]