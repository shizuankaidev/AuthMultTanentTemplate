from django.urls import path

from .views import (
    CompanyStoreListView,
    CompanyStoreCreateView,
    CompanyStoreUpdateView,
    CompanyStoreDeleteView,
)


urlpatterns = [
    path("", CompanyStoreListView.as_view(), name="store-list"),
    path("create/", CompanyStoreCreateView.as_view(), name="store-create"),
    path("<int:store_id>/", CompanyStoreUpdateView.as_view(), name="store-update"),
    path("<int:store_id>/delete/", CompanyStoreDeleteView.as_view(), name="store-delete"),
]