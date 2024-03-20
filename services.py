import stripe

import requests
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def get_session():
    """Функция создания платежной сессии"""
    product = stripe.Product.create(name='Test_course')

    price = stripe.Price.create(
        currency='rub',
        unit_amount=10000,
        product=f'{product.id}'
    )

    response = stripe.checkout.Session.create(
        success_url="https://example.com/success",
        line_items=[{"price": price, "quantity": 1}],
        mode="payment",
    )

    return response


class MyBot:
    """Класс для работы с уведомлениями в телеграм"""

    URL = f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}'

    def send_message(self, chat_id, text):
        path = f'{self.URL}/sendMessage'
        requests.post(
            url=path,
            data={
                'chat_id': chat_id,
                'text': text
            }
        )