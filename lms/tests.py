from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, CourseSubscriber
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@example.com")
        self.course = Course.objects.create(title="Course 1", description="Course 1")
        self.lesson = Lesson.objects.create(
            title="Lesson 1",
            description="Lesson 1",
            url="https://www.youtube.com/",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_detail(self):
        path = reverse("lms:lesson_detail", args=(self.lesson.pk, ))
        response = self.client.get(path)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        path = reverse("lms:lesson_create")
        data = {
            "title": "Lesson 2",
            "description": "Lesson 2",
            "url": "https://www.youtube.com/6587tgv",
            "course": self.course.pk,
        }
        response = self.client.post(path, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        path = reverse("lms:lesson_update", args=(self.lesson.pk, ))
        data = {"title": "Lesson 2"}
        response = self.client.patch(path, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.get(pk=self.lesson.pk).title, "Lesson 2")

    def test_lesson_delete(self):
        path = reverse("lms:lesson_delete", args=(self.lesson.pk, ))
        response = self.client.delete(path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("lms:lesson_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), 1)


class SubscribeTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@example.com")
        self.course = Course.objects.create(title="Course 1", description="Course 1")
        self.client.force_authenticate(user=self.user)
        self.path = reverse("lms:subscribe")

    def test_subscribe_create(self):
        data = {"course": self.course.pk}
        response = self.client.post(self.path, data)
        message = response.json().get('message')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(message, 'Подписка на курс Course 1 добавлена.')
        self.assertEqual(CourseSubscriber.objects.all().count(), 1)

    def test_subscribe_delete(self):
        CourseSubscriber.objects.create(user=self.user, course=self.course)
        data = {"course": self.course.id}
        response = self.client.post(self.path, data=data)
        message = response.json().get('message')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(message, 'Подписка на курс Course 1 удалена.')
        self.assertEqual(CourseSubscriber.objects.all().count(), 0)
