from rest_framework import serializers

from users.models import Payment, User, Subscription


class UserSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для модели пользователя"""

    class Meta:
        model = User
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для модели платежа"""

    class Meta:
        model = Payment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    """Базовый ериализатор для модели подписки"""

    class Meta:
        model = Subscription
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра профиля пользователя,
       включает поле истории платежей"""
    payment_list = PaymentSerializer(source='payment_set', many=True)

    class Meta:
        model = User
        fields = '__all__'


class PaymentCreateSerializer(serializers.ModelSerializer):
    """Cериализатор для создания платежа"""

    class Meta:
        model = Payment
        fields = ('payment_url',)