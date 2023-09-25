from rest_framework import serializers
from .models import Lesson

class LesssonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title','products','slug','video','length_video','last_time_view']
        
