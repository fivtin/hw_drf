from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from lms.models import Course, Lesson
from lms.permissions import IsModerator, IsOwner, IsNotModerator
# Create your views here.
from lms.serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from rest_framework import viewsets
from rest_framework import generics

from users.models import Payment


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    queryset = Course.objects.all()

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, IsNotModerator]
        elif self.action == 'retrieve':
            permission_classes = [IsOwner | IsModerator]
        elif self.action == 'update':
            permission_classes = [IsOwner | IsModerator]
        elif self.action == 'partial_update':
            permission_classes = [IsOwner | IsModerator]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwner]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


class LessonSerializerClassMixin:
    serializer_class = LessonSerializer


class LessonCreateAPIView(LessonSerializerClassMixin, generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(LessonSerializerClassMixin, generics.ListAPIView):
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(LessonSerializerClassMixin, generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator]


class LessonUpdateAPIView(LessonSerializerClassMixin, generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner, IsNotModerator]


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['paid_at']
    filterset_fields = ('course', 'lesson', 'method', )
    permission_classes = [IsAuthenticated]
