from lms.models import Course, Lesson
# Create your views here.
from lms.serializers import CourseSerializer, LessonSerializer
from rest_framework import viewsets
from rest_framework import generics


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class LessonSerializerClassMixin:
    serializer_class = LessonSerializer


class LessonCreateAPIView(LessonSerializerClassMixin, generics.CreateAPIView):
    ...


class LessonListAPIView(LessonSerializerClassMixin, generics.ListAPIView):
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(LessonSerializerClassMixin, generics.RetrieveAPIView):
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(LessonSerializerClassMixin, generics.UpdateAPIView):
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
