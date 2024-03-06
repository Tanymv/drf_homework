from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField

from materials.models import Course, Lesson
from materials.validators import url_validator


class CourseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для модели курса"""

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для модели урока"""
    url = serializers.URLField(validators=[url_validator])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseDetailSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра информации о курсе, включает в себя
       поля количества уроков, списка уроков этого курса и признак
       подписки текущего пользователя на этот курс (bool)"""
    lessons_count = SerializerMethodField()
    lessons_list = SerializerMethodField()
    is_subscribed = SerializerMethodField()

    def user_(self):
        """Получаем текущего пользователя"""
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_is_subscribed(self, course):
        """Проверяем, есть ли в наборе подписок курса объект
           с текущим пользователем"""
        return course.subscription_set.filter(user=self.user_()).exists()

    @staticmethod
    def get_lessons_count(course):
        """Получаем количество уроков для данного курса"""
        return Lesson.objects.filter(course=course).count()

    @staticmethod
    def get_lessons_list(course):
        """Получаем список уроков для данного курса"""
        return LessonSerializer(Lesson.objects.filter(course=course),
                                many=True).data

    class Meta:
        model = Course
        fields = '__all__'


class LessonDetailSerializer(serializers.ModelSerializer):
    """Cериализатор для просмотра информации об уроке,
       где для курса выводится его наименование"""
    course = SlugRelatedField(slug_field='name', queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = '__all__'