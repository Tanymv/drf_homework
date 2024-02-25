from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для модели курса"""

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для модели урока"""

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseDetailSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра информации о курсе, включает в себя поля количества уроков и
    списка уроков этого курса"""
    lessons_count = SerializerMethodField()
    lessons_list = SerializerMethodField()

    @staticmethod
    def get_lessons_count(course):
        return Lesson.objects.filter(course=course).count()

    @staticmethod
    def get_lessons_list(course):
        return LessonSerializer(Lesson.objects.filter(course=course), many=True).data

    class Meta:
        model = Course
        fields = '__all__'