from django.urls import path
from . import views


urlpatterns = [
    path('', views.TransactionListAPIView.as_view(), name="transactions"),
    path('<str:transaction_id>', views.TransactionDetailAPIView.as_view(), name="transaction")
]