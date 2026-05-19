from django.urls import re_path

from core.views import proxy

urlpatterns = [
    re_path(r"^(?P<path>.*)$", proxy),
]
