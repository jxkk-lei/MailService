from django.urls import path
from . import views

app_name = "mailing_lists"

urlpatterns = [
    path("", views.list_view, name="list"),
]