from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson
# Create your views here.
from lms.serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from rest_framework import viewsets
from rest_framework import generics

from users.models import Payment


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
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


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['paid_at']
    filterset_fields = ('course', 'lesson', 'method', )
