from django.urls import path, include
from rest_framework.routers import DefaultRouter

from lms.apps import LmsConfig
from lms.views import CourseViewSet, LessonListAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, \
    LessonDestroyAPIView, LessonCreateAPIView, PaymentListAPIView, CourseSubscriberAPIView

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lessons/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lessons/create', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_detail'),
    path('lessons/<int:pk>/update', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lessons/<int:pk>/delete', LessonDestroyAPIView.as_view(), name='lesson_delete'),
    path('payments/', PaymentListAPIView.as_view(), name='payment_list'),
    path("subscribe/", CourseSubscriberAPIView.as_view(), name="subscribe"),
] + router.urls
