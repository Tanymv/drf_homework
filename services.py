import stripe
from config import settings


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