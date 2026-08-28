from django.urls import path

from .views import LoginView, RegisterView, ProfileView, RefreshView
from .viewAdmin import AdminUserListView, AdminUserUpdateView


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshView.as_view(), name="refresh"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),

    path("admin/users/", AdminUserListView.as_view(), name="admin-user-list"),
    path("admin/users/<int:user_id>/", AdminUserUpdateView.as_view(), name="admin-user-update"),
]