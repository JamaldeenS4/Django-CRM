from django.contrib import admin
from django.urls import path, include
from leads import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('leads/', include('leads.urls'))
]
