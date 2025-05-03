from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('invoices/', include('invoices.urls')),  # d'abord les vraies routes
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/admin/login/', permanent=False)),  # ensuite la redirection par défaut

]
