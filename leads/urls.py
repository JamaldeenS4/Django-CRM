from django.urls import path
from . import views

app_name ='leads'
urlpatterns = [
    path("", views.LeadList.as_view(), name='list'),
    path("<int:pk>/", views.LeadDetail.as_view(), name='detail'),
    path("create/", views.LeadCreate.as_view(), name='create'),
    path("<int:pk>/update/", views.LeadUpdate.as_view(), name='update'),
    path("<int:pk>/delete/", views.LeadDelete.as_view(), name='delete'),
    path("<int:pk>/assign-agent/", views.AssignAgentView.as_view(), name='assign-agent'),
    path("<int:pk>/category/", views.LeadCategoryUpdateView.as_view(), name='lead-category-update'),
    path("categories/", views.CategoryListView.as_view(), name='category-list'),
    path("categories/<int:pk>/", views.CategoryDetailView.as_view(), name='category-detail'),

]