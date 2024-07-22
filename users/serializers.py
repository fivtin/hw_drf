from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.serializers import ModelSerializer

from lms.serializers import CourseSerializer
from users.models import User, Payment


class JWTTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавление пользовательских полей в токен
        token['username'] = user.username
        token['email'] = user.email

        return token


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'city', 'image', ]


class UserRetrieveSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'city', 'image', ]


class CreateCoursePaymentSerializer(ModelSerializer):
    # course = serializers.IntegerField(required=True, min_value=0)
    # session_id = serializers.CharField(read_only=True)
    # link = serializers.CharField(read_only=True)

    class Meta:
        model = Payment
        fields = ['course', 'amount', 'session_id', 'link', ]
        extra_kwargs = {'course': {'required': True}}
        read_only_fields = ['session_id', 'link', ]
