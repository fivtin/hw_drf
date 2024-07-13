from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.apps import UsersConfig
from users.views import UserCreateView, email_confirm, reset_password, reset_password_success, UserListView, \
    user_deactivate, user_activate, JWTTokenObtainPairView, UserCreateAPIView, UserUpdateAPIView, UserRetrieveAPIView, \
    UserDestroyAPIView

app_name = UsersConfig.name


urlpatterns = [
    path('login', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register/confirm/<str:token>', email_confirm, name='confirm'),
    path('register', UserCreateView.as_view(), name='register'),
    path('register/reset-password-success', reset_password_success, name='reset-password-success'),
    path('register/reset-password', reset_password, name='reset-password'),
    path('', UserListView.as_view(), name='list'),
    path('<int:id>/deactivate', user_deactivate, name='deactivate'),
    path('<int:id>/activate', user_activate, name='activate'),
    path('token/', JWTTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api_register/', UserCreateAPIView.as_view(), name='api_register'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='api_detail'),
    path('<int:pk>/update/', UserUpdateAPIView.as_view(), name='api_update'),
    path('<int:pk>/delete/', UserDestroyAPIView.as_view(), name='api_delete'),
]
