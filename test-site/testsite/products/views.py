from django.shortcuts import render, get_object_or_404
from .models import Product, Lesson, Access
from backend.models import LessonViewing
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


@login_required
def catalog(request):
    title = 'Продукты'
    access = Access.objects.filter(user=request.user).values('product__id')
    products = Product.objects.filter(Q(id__in=access))
    return render(request, 'products/catalog.html', {'title': title, 'products': products})


@login_required
def lessons(request, product_id):
    title = 'Уроки'
    access = Access.objects.filter(user=request.user).values('product__id')
    products = Product.objects.filter(id=product_id).filter(Q(id__in=access))
    
    for p in products:
        product_cat = p
    lessons = Lesson.objects.filter(products=product_cat)
    return render(request, 'products/lessons.html', {'title': title, 'products': products, 'lessons': lessons})


@login_required
def lesson_detail(request, product_id, lesson_id):
    title = 'Урок'
    access = Access.objects.filter(user=request.user).values('product__id')
    lesson = get_object_or_404(Lesson, id=lesson_id)
    product = Product.objects.filter(id=product_id).filter(Q(id__in=access))
    video_id = lesson.video[32:43:]
    Viewing, created = LessonViewing.objects.get_or_create(
        user=request.user, lesson=lesson)
    Viewing.save()
    return render(request, 'products/lesson_detail.html', {'title': title, 'product': product, 'lesson': lesson, 'video_id': video_id})



@csrf_exempt
def video_moment(request):
    if request.method == 'POST':
        moment = float(request.POST.get('moment'))
        lesson_id = request.POST.get('lesson_id')
        lesson = get_object_or_404(Lesson, id=lesson_id)
        Viewing, created = LessonViewing.objects.get_or_create(
        user=request.user, lesson=lesson)
        if Viewing.duration_viewed < moment:
            Viewing.duration_viewed = moment
            Viewing.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})