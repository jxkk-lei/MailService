from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("", views.list_view, name="list"),
    path("<int:user_id>/", views.detail_view, name="detail"),
]
