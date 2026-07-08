import random

from datetime import datetime
from datetime import timedelta

from faker import Faker

from backend.constants.demo_data import (
    CITIES,
    STATES,
    COUNTRY,
    GENDERS,
    PAYMENT_METHODS,
    TRANSACTION_STATUS,
    PRODUCTS,
    CATEGORY_PRICE_RANGE,
    MIN_AGE,
    MAX_AGE,
)

fake = Faker("en_IN")

def random_name():
    return fake.name()

def random_email(name: str):

    username = (
        name.lower()
        .replace(" ", ".")
    )

    number = random.randint(1, 999)

    domains = [
    "gmail.com",
    "outlook.com",
    "yahoo.com",
    ]

    return (
    f"{username}{number}@"
    f"{random.choice(domains)}"
    )

def random_phone():
    return str(
        random.randint(
          6000000000,
          9999999999,  
        )
    )

def random_gender():
    return random.choice(GENDERS)

def random_age():
    return random.randint(
        MIN_AGE,
        MAX_AGE,
    )

def random_city():
    return random.choice(CITIES)

def random_state():
    return random.choice(STATES)

def random_country():
    return COUNTRY

def random_product():

    category = random.choice(
        list(PRODUCTS.keys())
    )

    product = random.choice(
        PRODUCTS[category]
    )

    return category, product

def random_amount(category):

    minimum, maximum = (
        CATEGORY_PRICE_RANGE[category]
    )

    return round(
        random.uniform(
            minimum,
            maximum,
        ),
        2,
    )

def random_quantity():

    return random.randint(
        1,
        5,
    )

def random_payment_method():

    return random.choice(
        PAYMENT_METHODS
    )

def random_transaction_status():

    return random.choice(
        TRANSACTION_STATUS
    )

def random_transaction_date():

    days = random.randint(
        0,
        730,
    )

    return (
        datetime.utcnow()
        - timedelta(days=days)
    )

def random_postal_code():

    return fake.postcode()

def customer_code(
    organization_code,
    number,
):

    return (
        f"{organization_code}"
        f"-CUST-"
        f"{number:04d}"
    )

def transaction_code(
    organization_code,
    number,
):

    return (
        f"{organization_code}"
        f"-TXN-"
        f"{number:06d}"
    )
def random_transaction_count():

    return random.randint(5, 15)