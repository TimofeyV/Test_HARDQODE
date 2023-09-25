from rest_framework.serializers import ModelSerializer, BooleanField, IntegerField, FloatField, DateTimeField, CharField
from products.models import Product, Lesson


class ProductSerializer(ModelSerializer):
    '''Сериализатор для продуктов'''

    class Meta:
        model = Product
        fields = ('id', 'title')


class ProductsStatisticsSerializer(ProductSerializer):
    """Сериализатор для вывода статистики по продуктам (образовательным
    программам)."""

    lesson_viewed_count = IntegerField(read_only=True)
    duration_viewed_sum = IntegerField(read_only=True)
    user_count = IntegerField(read_only=True)
    purchase_percentage = FloatField(read_only=True)

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + (
            'lesson_viewed_count', 'duration_viewed_sum',
            'user_count', 'purchase_percentage'
        )


class LessonSerializer(ModelSerializer):
    '''Сериализатор для уроков'''

    is_viewed = BooleanField(read_only=True)
    percentage_viewed= FloatField(read_only=True)
    product = CharField(read_only=True)
    class Meta:
        model = Lesson
        fields = ('id', 'title','product', 'video',
                  'duration', 'percentage_viewed',
                  'is_viewed')
        

class ProductLessonSerializer(ModelSerializer):
    '''Сериализатор для уроков'''
    is_viewed = BooleanField(read_only=True)
    duration_viewed = IntegerField(read_only=True)
    percentage_viewed= FloatField(read_only=True)
    last_viewed = DateTimeField(read_only=True)

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'video',
                  'duration','duration_viewed', 'percentage_viewed',
                  'is_viewed', 'last_viewed')