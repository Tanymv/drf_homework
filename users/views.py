import stripe
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings
from materials.models import Course
from services import get_session
from users.models import User, Payment, Subscription
from users.serializers import UserSerializer, PaymentSerializer, UserDetailSerializer, SubscriptionSerializer, \
    PaymentCreateSerializer


class UserCreateView(generics.CreateAPIView):
    """Регистрация нового пользователя"""
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Переопределение метода для сохранения хешированного пароля в бд (если пароль не хешируется -
        пользователь не считается активным и токен авторизации не создается)"""
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        password = serializer.data["password"]
        user = User.objects.get(pk=serializer.data["id"])
        user.set_password(password)
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserDetailView(generics.RetrieveAPIView):
    """Просмотр профиля пользователя"""
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()


class UserUpdateView(generics.UpdateAPIView):
    """Редактирование профиля пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDeleteView(generics.DestroyAPIView):
    """Удаление профиля пользователя"""
    queryset = User.objects.all()


class UserListView(generics.ListAPIView):
    """Просмотр списка зарегистрированных пользователей"""
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PaymentListView(generics.ListAPIView):
    """Просмотр списка платежей с фильтрацией по курсу, уроку и способу оплаты,
    и с сортировкой по дате(по умолчанию в модели сортировка по убыванию, при запросе можно изменить с помощью -)"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ('payment_date',)


class PaymentCreateView(generics.CreateAPIView):
    """Создание платежа"""
    serializer_class = PaymentCreateSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        stripe.api_key = settings.STRIPE_API_KEY
        response = get_session()
        new_payment = serializer.save()
        new_payment.session_id = response['id']
        new_payment.payment_url = response['url']
        new_payment.payment_status = response['payment_status']
        new_payment.payment_amount = response['amount_total']
        new_payment.save()
        return super().perform_create(serializer)


class SubscriptionView(APIView):
    """Контроллер управления подпиской пользователя на курс
       в запросе передаем id курса и если подписка на данный курс у текущего пользователя
       существует - удаляем, если нет - создаем"""
    serializer_class = SubscriptionSerializer

    @staticmethod
    def post(request, pk):
        queryset = Course.objects.filter(pk=pk)
        user = request.user
        course = get_object_or_404(queryset=queryset)
        subs_item = Subscription.objects.filter(course=course, user=user)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'
        return Response({"message": message})