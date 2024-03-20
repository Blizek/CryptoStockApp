from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TransactionSerializer
from .models import Transaction, User
from rest_framework import permissions
from utils.user_permissions import IsOwner

# Create your views here.


class TransactionListAPIView(ListCreateAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = (permissions.IsAuthenticated,)


    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class TransactionDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    queryset = Transaction.objects.all()
    lookup_field = "transaction_id"

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
