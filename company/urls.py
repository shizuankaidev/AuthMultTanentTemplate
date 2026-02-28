from django.urls import path
from .viewsAdmin import CompanyAdminViewSet


company_list = CompanyAdminViewSet.as_view({
    "get": "list",
    "post": "create",
})

company_detail = CompanyAdminViewSet.as_view({
    "get": "retrieve",
    "put": "update",
    "patch": "partial_update",
    "delete": "destroy",
})

company_owner = CompanyAdminViewSet.as_view({
    "post": "set_owner",
    "delete": "revoke_owner",
})


urlpatterns = [
    path("", company_list, name="company-list"),
    path("<int:pk>/", company_detail, name="company-detail"),
    path("<int:pk>/owner/", company_owner, name="company-owner"),
]