from django.urls import path
from . import views


urlpatterns = [
    path('', views.AssetsListAPIView.as_view(), name="assets"),
]