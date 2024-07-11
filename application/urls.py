from django.urls import path
from .views import (
    CreateDriversLicenseApplicationView,
    RenewDriversLicenseApplicationView,
    ReissueDriversLicenseApplicationView,
)

urlpatterns = [
    path('applications/create/', CreateDriversLicenseApplicationView.as_view(), name='create_application'),
    path('applications/renew/<str:license_id>/', RenewDriversLicenseApplicationView.as_view(), name='renew_application'),
    path('applications/reissue/<str:license_id>/', ReissueDriversLicenseApplicationView.as_view(), name='reissue_application'),
]

