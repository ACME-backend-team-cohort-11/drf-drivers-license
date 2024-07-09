# portal/urls.py
from django.urls import path
from .views import LicenseValidityView, LicenseDetailsView

urlpatterns = [
    path('licenses/<int:pk>/validity/', LicenseValidityView.as_view(), name='license_validity'),
    path('licenses/<int:pk>/', LicenseDetailsView.as_view(), name='license_details'),
]

