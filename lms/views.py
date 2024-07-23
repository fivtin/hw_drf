from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course, Lesson, CourseSubscriber
from lms.paginators import CoursePagination, LessonPagination, PaymentPagination
from lms.permissions import IsModerator, IsOwner, IsNotModerator
# Create your views here.
from lms.serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from rest_framework import viewsets
from rest_framework import generics

from users.models import Payment


class CourseViewSet(viewsets.ModelViewSet):
    """Implementation of CRUD API for courses."""

    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    queryset = Course.objects.all()
    pagination_class = CoursePagination

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

    def get_queryset(self):
        if IsModerator().has_permission(self.request, self):
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


class LessonSerializerClassMixin:
    serializer_class = LessonSerializer


class LessonCreateAPIView(LessonSerializerClassMixin, generics.CreateAPIView):
    """Create lesson."""

    permission_classes = [IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """Get a list of lessons."""

    queryset = Lesson.objects.all()
    pagination_class = LessonPagination

    def get_queryset(self):
        if IsModerator().has_permission(self.request, self):
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(LessonSerializerClassMixin, generics.RetrieveAPIView):
    """Get detailed information about the lesson."""

    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator]


class LessonUpdateAPIView(LessonSerializerClassMixin, generics.UpdateAPIView):
    """Update lesson."""

    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Delete lesson."""

    queryset = Lesson.objects.all()
    permission_classes = [IsOwner, IsNotModerator]


class PaymentListAPIView(generics.ListAPIView):
    """Get a list of payments."""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['paid_at']
    filterset_fields = ('course', 'lesson', 'method', )
    permission_classes = [IsAuthenticated]
    pagination_class = PaymentPagination


class CourseSubscriberAPIView(APIView):
    """Subscribe to the course. / Unsubscribe from the course."""

    @swagger_auto_schema(operation_description='Send the "course" parameter with the ID value in the request body.')
    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = CourseSubscriber.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = f'Подписка на курс {course_item.title} удалена.'
        else:
            CourseSubscriber.objects.create(user=user, course=course_item)
            message = f'Подписка на курс {course_item.title} добавлена.'

        return Response({"message": message})
