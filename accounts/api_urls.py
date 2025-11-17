from django.urls import path
from .views_api import accounts_root, RegisterView, UserDetailView

urlpatterns = [
    path("", accounts_root),
    path("register/", RegisterView.as_view(), name="api_register"),
    path("me/", UserDetailView.as_view(), name="api_me"),
]
