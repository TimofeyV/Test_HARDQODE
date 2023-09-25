import rest_framework
from products.models import Access

class AccessSerializer(rest_framework.ModelSerializer):
    class Meta:
        model = Access
        fields = 'all'