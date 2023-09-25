from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from django.shortcuts import get_object_or_404
from django.db import models
from django.db.models.functions import Coalesce
from django.db.models import OuterRef, Subquery, Count, Q, Sum
from django.contrib.auth.models import User


from products.models import Product, Lesson, Access
from backend.models import LessonViewing
from .serializers import *


class StaticticsViewSet(ReadOnlyModelViewSet):
    """Получение колличества учеников занимающихся на продукте"""
    serializer_class = ProductsStatisticsSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AllowAny, )
    
    def get_queryset(self):
        all_users = User.objects.all().count()
        return Product.objects.prefetch_related(
            'related_assigments', 
            'related_lessons__related_views'
        ).annotate(
            user_count = Coalesce(
                Count(
                    'related_assigments',
                ),0, output_field=models.IntegerField()

            ),
            purchase_percentage = Coalesce(
                Count(
                    'related_assigments',distinct=True,
                )*100/all_users, 0, output_field=models.FloatField()
            ),
            duration_viewed_sum = Coalesce(
                Sum(
                    'related_lessons__related_views__duration_viewed',
                ),0, output_field=models.IntegerField()
            ),
            lesson_viewed_count = Coalesce(
                Count(
                    'related_lessons__related_views', distinct=True,
                    filter=Q(
                        related_lessons__related_views__in=Subquery(
                            LessonViewing.objects.filter(
                                is_viewed = True
                            ).values('id'),
                        )

                    )
                ),0, output_field=models.IntegerField()
            )
        )
    

class UserLessonsViewSet(ListModelMixin, GenericViewSet):
    """Получение списка уроков для указанного пользователя по id"""
    serializer_class = LessonSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AllowAny,)

    def get_queryset(self):
        user = get_object_or_404(User.objects.only('id'), pk=self.kwargs.get('user_id'))
        product_ids = Product.objects.filter(viewer = user).values('id')
        return Lesson.objects.filter(Q(products__in=product_ids)).annotate(
            product = Coalesce(
                Subquery(
                    Product.objects.filter(
                        related_lesson=OuterRef('pk'),
                        viewer=user
                    ).values('title')[:1],
                ), 0, output_field=models.CharField()
            ),
            duration_viewed=Coalesce(
                Subquery(
                    LessonViewing.objects.filter(
                        lesson=OuterRef('pk'),
                        user=user
                    ).values('duration_viewed')[:1],
                ), 0, output_field=models.IntegerField()
            ),
            percentage_viewed=Coalesce(
                Subquery(
                    LessonViewing.objects.filter(
                        lesson=OuterRef('pk'),
                        user=user
                    ).values('percentage_viewed')[:1],
                ), 0, output_field=models.FloatField()
            ),
            is_viewed=Coalesce(
                Subquery(
                    LessonViewing.objects.filter(
                        lesson=OuterRef('pk'),
                        user=user
                    ).values('is_viewed')[:1],
                ), False, output_field=models.BooleanField()
            ),
        ).distinct().order_by('id')


class UserProductLessonsViewSet(ListModelMixin, GenericViewSet):
    """Получение списка уроков для указанного пользователя по id и продукта по id"""
    serializer_class = ProductLessonSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AllowAny,)

    def get_queryset(self):
        user = get_object_or_404(User.objects.only('id'), pk=self.kwargs.get('user_id'))
        product = get_object_or_404(Product, pk = self.kwargs.get('product_id'))
        if not product.viewer.filter(username=user.username).exists():
            return {}
        return Lesson.objects.filter(Q(products = product)).annotate(
                duration_viewed=Coalesce(
                    Subquery(
                        LessonViewing.objects.filter(
                            lesson=OuterRef('pk'),
                            user=user
                        ).values('duration_viewed')[:1],
                    ), 0, output_field=models.IntegerField()
                ),
                percentage_viewed=Coalesce(
                    Subquery(
                        LessonViewing.objects.filter(
                            lesson=OuterRef('pk'),
                            user=user
                        ).values('percentage_viewed')[:1],
                    ), 0, output_field=models.FloatField()
                ),
                is_viewed=Coalesce(
                    Subquery(
                        LessonViewing.objects.filter(
                            lesson=OuterRef('pk'),
                            user=user
                        ).values('is_viewed'),
                    ), False, output_field=models.BooleanField()
                ),
                last_viewed=Coalesce(
                    Subquery(
                        LessonViewing.objects.filter(
                            lesson=OuterRef('pk'),
                            user=user
                        ).values('last_viewed')[:1],
                    ), None, output_field=models.DateTimeField()
                ),
            ).distinct().order_by('id')