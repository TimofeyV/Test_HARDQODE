from products.models import *
from .serializers import *

class AccessListView(generics.ListAPIView):
    queryset = Access.objects.all()
    serializer_class = serializers.AccessSerializer


class AccessDetailView(generics.RetrieveAPIView):
    queryset = Access.objects.all()
    serializer_class = serializers.AccessSerializer