from django.contrib import admin
from django.urls import include, path

handler404 = "homepage.views.not_found"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("users/", include("users_web.urls")),
    path("lists/", include("mailing_lists_web.urls")),
    path("messages/", include("messages_web.urls")),
    path("subscriptions/", include("subscriptions_web.urls")),
]
