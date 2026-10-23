from django.urls import path
from . import views

app_name = "messages"

urlpatterns = [
    path("", views.list_view, name="list"),
    path("<int:message_id>/", views.detail_view, name="detail"),
]
