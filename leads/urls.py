from django.urls import path
from . import views

app_name ='leads'
urlpatterns = [
    path("", views.LeadList.as_view(), name='list'),
    path("<int:pk>/", views.LeadDetail.as_view(), name='detail'),
    path("create/", views.LeadCreate.as_view(), name='create'),
    path("<int:pk>/update/", views.LeadUpdate.as_view(), name='update'),
    path("<int:pk>/delete/", views.LeadDelete.as_view(), name='delete')
]