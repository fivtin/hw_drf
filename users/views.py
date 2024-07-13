import string
import secrets
import random

from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm
from users.models import User
from users.permissions import IsOwner
from users.serializers import JWTTokenObtainPairSerializer, UserSerializer, UserUpdateSerializer, UserRetrieveSerializer


# Create your views here.

class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):

        user = form.save()
        user.is_active = False
        token = secrets.token_hex(32)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/register/confirm/{token}'
        try:
            send_mail(
                subject='Подтверждение регистрации.',
                message=f'Для подтверждения регистрации перейдите по ссылке {url}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email]
            )
        except Exception as e:
            print(e)
        return super().form_valid(form)


def email_confirm(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True

    user.save()
    return redirect(reverse('users:login'))


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = get_object_or_404(User, email=email)
        characters = string.ascii_letters + string.digits  # + string.punctuation
        password = ''.join(random.choice(characters) for i in range(8))
        send_mail(
            subject='Восстановление пароля.',
            message=f'Для учетной записи {email} был установлен новый пароль: {password}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[email]
        )
        user.set_password(password)
        user.save()
        return redirect(reverse('users:reset-password-success'))

    return render(request, 'users/reset_password.html')


def reset_password_success(request):
    return render(request, 'users/reset_password_success.html')


class UserListView(PermissionRequiredMixin, ListView):
    model = User

    permission_required = 'users.view_list'

    def get_queryset(self):
        queryset = User.objects.filter(is_superuser=False).exclude(id=self.request.user.id)
        return queryset


@login_required
@permission_required('users.change_active')
def user_deactivate(request, id):
    user = get_object_or_404(User, pk=id)

    if not user.is_superuser:
        user.is_active = False
        user.save()
    return redirect(reverse('users:list'))


@login_required
@permission_required('users.change_active')
def user_activate(request, id):
    user = get_object_or_404(User, pk=id)
    user.is_active = True
    user.save()
    return redirect(reverse('users:list'))


class JWTTokenObtainPairView(TokenObtainPairView):
    serializer_class = JWTTokenObtainPairSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwner]


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserRetrieveSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
