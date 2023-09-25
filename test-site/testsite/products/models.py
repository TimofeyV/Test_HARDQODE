from django.db import models
from django.utils.text import slugify
from django.urls import reverse
import pytube



class BaseModel(models.Model):
    """Базовая абстрактная модель"""
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    created = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='дата создания')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='дата обновления')

    class Meta:
        abstract = True


class Owner(BaseModel):
    """Модель владельцев продуктов"""
    name = models.CharField(max_length=255, unique=True,
                            verbose_name='имя')

    class Meta:
        verbose_name = 'владелец'
        verbose_name_plural = 'владельцы'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Product(BaseModel):
    """Модель продуктов"""
    title = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:product', args=[self.slug])


class Lesson(BaseModel):
    """Модель уроков"""
    title = models.CharField(max_length=100, verbose_name='Название', )
    products = models.ManyToManyField(Product,related_name='related_lessons', verbose_name='Продукты в которых содержится')
    slug = models.SlugField(max_length=200, db_index=True)
    video = models.URLField(verbose_name='Ссылка на видео')
    duration = models.IntegerField(verbose_name='Длительность(сек)')


    class Meta:
        ordering = ('title',)
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.duration = pytube.YouTube(self.video).length
        if not self.slug:
            self.slug = slugify(self.title)
        super(Lesson, self).save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('product:lesson', kwargs={'slug': self.slug})


class Access(models.Model):
    """Модель доступа"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='related_assigments')
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='related_assigments')

    class Meta:
        unique_together = ('product', 'user')

    def str(self):
        if self.user:
            return f'Доступ пользователю {self.user.username} к продукту {self.product.name}'
        else:
            return 'Доступ без пользователя (например, админу)'
    def get_queryset(self):
        qs = super().get_querset()
        product_id = self.kwargs['pk']
        user_pk = self.request.user.pk
        try:
            Access.objects.get(product_id=product_id, user_id=user_pk)
        except Access.DoesNotExist:
            raise PermissionDenied
        return qs
    
    class Meta:
        verbose_name = 'Доступ'
        verbose_name_plural = 'Доступы'