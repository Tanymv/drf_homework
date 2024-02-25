from django.contrib import admin

from materials.models import Course, Lesson


# admin.site.register(Course)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description', 'owner')


# admin.site.register(Lesson)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description', 'owner')