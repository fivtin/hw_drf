from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from lms.models import Course, Lesson, CourseSubscriber
from lms.validators import YoutubeValidator
from users.models import Payment


class LessonSerializer(serializers.ModelSerializer):
    # course = CourseSerializer(read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [YoutubeValidator(field="url")]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'preview', 'lesson_count', 'lessons', 'subscribed', )

    def get_lesson_count(self, instance):
        return Lesson.objects.filter(course=instance).count()

    def get_subscribed(self, course):
        return CourseSubscriber.objects.filter(course=course, user=self.context["request"].user).exists()


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class CourseSubscriberSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseSubscriber
        fields = '__all__'
