from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q, F, Case, When, Value, ExpressionWrapper

from products.models import Lesson, Product


class LessonViewingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            percentage_viewed=ExpressionWrapper(
                F('duration_viewed') * 100 / F('lesson__duration'),output_field=models.FloatField()),
            is_viewed=Case(
                When(
                    Q(percentage_viewed__gte=settings.VIEW_THRESHOLD),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=models.BooleanField()
            )
        )


class LessonViewing(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT,
                             related_name='related_views')
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT,
                               related_name='related_views')
    duration_viewed = models.PositiveIntegerField(
        default=0,
        verbose_name='просмотренно (сек)',
        help_text=('Продолжительность просмотре видео в секундах')
    )
    started = models.DateTimeField(auto_now=False, auto_now_add=True,
                                   verbose_name='дата начала просмотра')
    last_viewed = models.DateTimeField(auto_now=True, auto_now_add=False,
                                       verbose_name='дата последнего '
                                                    'просмотра')
    objects = LessonViewingManager()

    class Meta:
        verbose_name = 'просмотр урока'
        verbose_name_plural = 'просмотры уроков'
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(fields=['user', 'lesson'],
                                    name='unique_user_lesson_view'),
            ]

    def __str__(self):
        return f'{self.user.username} / {self.lesson.title}'