from rest_framework.generics import ListCreateAPIView
from .models import Asset
from rest_framework import permissions
from .serializers import AssetSerializer
from utils.user_permissions import IsOwner
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


# Create your views here.

class AssetsListAPIView(APIView):
    serializer_class = AssetSerializer
    queryset = Asset.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get(self, request):
        data = AssetSerializer(self.queryset.filter(owner=request.user), many=True).data
        for d in data:
            d.update({'test': 'dupa'})
            # otrzymywanie id krypto do uzyskania danych z zewnętrznego API
            # d_items = list(d.items())
            # print(d_items)
            # print(d_items[1][1])
        return Response({'data': data}, status=status.HTTP_200_OK)
