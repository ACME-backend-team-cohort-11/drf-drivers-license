# portal/urls.py
from django.urls import path
from .views import LicenseDetailView

urlpatterns = [
        path('licenses/<str:license_id>/', LicenseDetailView.as_view(), name='license_detail'),


]

