from django.urls import path

from .views import ThanksPageView, get_info_view

urlpatterns = [
    path("", get_info_view, name="get_info"),
    path("thanks/", ThanksPageView.as_view(), name="thanks"),
]
