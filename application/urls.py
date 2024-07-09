from django.urls import path
from .views import (
    CreateDriversLicenseApplicationView,
    RenewDriversLicenseApplicationView,
    ReissueDriversLicenseApplicationView,
    ListDriversLicenseApplicationsView,
    RetrieveDriversLicenseApplicationView,
)

urlpatterns = [
    path('applications/create/', CreateDriversLicenseApplicationView.as_view(), name='create_application'),
    path('applications/renew/<uuid:pk>/', RenewDriversLicenseApplicationView.as_view(), name='renew_application'),
    path('applications/reissue/<uuid:pk>/', ReissueDriversLicenseApplicationView.as_view(), name='reissue_application'),
    path('applications/', ListDriversLicenseApplicationsView.as_view(), name='list_applications'),
    path('applications/<uuid:pk>/', RetrieveDriversLicenseApplicationView.as_view(), name='retrieve_application'),
]

