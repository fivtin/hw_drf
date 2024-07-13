from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from lms.models import Course, Lesson
from users.models import Payment


class LessonSerializer(serializers.ModelSerializer):
    # course = CourseSerializer(read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'preview', 'lesson_count', 'lessons', )

    def get_lesson_count(self, instance):
        return Lesson.objects.filter(course=instance).count()


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'
