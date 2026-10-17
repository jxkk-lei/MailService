from django.contrib import admin
from django.urls import include, path
from homepage.views import index

handler404 = "homepage.views.not_found"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="home"),
    path("users/", include("users_web.urls")),
    path("lists/", include("mailing_lists_web.urls")),
    path("messages/", include("messages_web.urls")),
    path("subscriptions/", include("subscriptions_web.urls")),
]