from django.contrib import admin

from .models import LessonViewing



@admin.register(LessonViewing)
class LessonViewing(admin.ModelAdmin):
    list_display = ('id', 'user', 'lesson', 'percentage_viewed', 'is_viewed')
    list_display_links = ('id', 'user', 'lesson',)
    list_filter = ('started', 'last_viewed')
    readonly_fields = ('id', 'percentage_viewed', 'is_viewed', 'started',
                       'last_viewed')
    actions_selection_counter = True
    show_full_result_count = True
    @admin.display(boolean=True, description='Статус “Просмотрено”', )
    def is_viewed(self, obj):
        return obj.is_viewed

    @admin.display(description='просмотренно %')
    def percentage_viewed(self, obj):
        print(obj.percentage_viewed)
        return obj.percentage_viewed