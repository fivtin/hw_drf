import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stipe_session(price):
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
    )
    return session.id, session.url


def create_stripe_price(product, amount):
    return stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product=product.id,
    )


def create_stripe_product(name):
    return stripe.Product.create(name=name)


def create_stripe_payment_url(title, amount):
    product = create_stripe_product(title)
    price = create_stripe_price(product, amount)
    return create_stipe_session(price)
