from sqlalchemy.orm import Session

from backend.constants.demo_data import ORGANIZATIONS
from backend.core.security import hash_password

from backend.models.organization import Organization
from backend.models.user import User

from backend.schemas.auth import UserRole
from backend.repositories.auth_repository import AuthRepository
from backend.repositories.customer_repository import CustomerRepository
from backend.repositories.transaction_repository import TransactionRepository

from backend.constants.demo_data import (
    ORGANIZATIONS,
    ADMIN_USERS,
)

from backend.constants.seed_config import (
    DEFAULT_PASSWORD,
)
from backend.utils.fake_data import (
    random_name,
    random_email,
    random_phone,
    random_gender,
    random_age,
    random_city,
    random_state,
    random_country,
    random_postal_code,
    customer_code,
)

from backend.models.customer import Customer

from backend.constants.seed_config import (
    CUSTOMERS_PER_ORGANIZATION,
)
import random
from backend.models.transaction import Transaction
from backend.constants.demo_data import (
    PRODUCTS,
    INDUSTRY_CATEGORIES,
)
from backend.utils.fake_data import (
    random_transaction_count,
    random_amount,
    random_payment_method,
    random_quantity,
    random_transaction_status,
    random_transaction_date,
    transaction_code,
)
class DemoDataService:

    def __init__(self, db: Session):

        self.db = db

        self.auth_repository = AuthRepository(db)

        self.customer_repository = CustomerRepository(db)

        self.transaction_repository = TransactionRepository(db)

        self.organizations = {}

    def create_organizations(self):

        self.organizations = {}

        for data in ORGANIZATIONS:

            organization = self.auth_repository.get_organization_by_email(
                data["email"]
            )

            # If already exists, store it and continue
            if organization:

                self.organizations[organization.email] = organization

                continue

            # Otherwise create it
            organization = Organization(
                code=data["code"],
                slug=data["slug"],
                name=data["name"],
                industry=data["industry"],
                email=data["email"],
            )

            organization = self.auth_repository.create_organization(
                organization
            )

            self.organizations[organization.email] = organization

    def create_admin_users(self):

            for admin in ADMIN_USERS:

                existing = self.auth_repository.get_user_by_email(
                    admin["email"]
                )

                if existing:
                    continue

                organization = self.organizations.get(
                    admin["organization_email"]
                )

                if organization is None:
                    continue

                user = User(
                    org_id=organization.id,
                    name=admin["name"],
                    email=admin["email"],
                    password_hash=hash_password(DEFAULT_PASSWORD),
                    role=UserRole.ADMIN.value,
                )

                self.auth_repository.create_user(user)

                

    def create_customers(
        self,
        organization,
    ):

        # Check if this organization is already seeded
        count = self.customer_repository.get_customer_count(
            organization.id
        )

        if count >= CUSTOMERS_PER_ORGANIZATION:

            print(
                f"{organization.name}: already seeded."
            )

            return self.customer_repository.get_all_by_organization(
                organization.id
            )

        customers = []
        last_customer = self.customer_repository.get_last_customer(
            organization.id
        )

        if last_customer:

            customer_number = (
                int(
                    last_customer.customer_code.split("-")[-1]
                )
                + 1
            )

        else:

            customer_number = 1

        for _ in range(CUSTOMERS_PER_ORGANIZATION):

            name = random_name()

            customer = Customer(

                org_id=organization.id,

                customer_code=customer_code(
                    organization.code,
                    customer_number,
                ),

                name=name,

                email=random_email(name),

                phone=random_phone(),

                gender=random_gender(),

                age=random_age(),

                city=random_city(),

                state=random_state(),

                country=random_country(),

                postal_code=random_postal_code(),

            )

            customers.append(customer)

            customer_number += 1

        self.customer_repository.create_many(customers)

        print(
            f"{organization.name}: "
            f"{len(customers)} customers created."
        )

        return customers
        
    def create_transactions(
        self,
        organization,
        customers,
    ):

        existing = self.transaction_repository.get_transaction_count(
            organization.id
        )

        if existing > 0:

            print(
                f"{organization.name}: Transactions already exist."
            )

            return

        transactions = []

        transaction_number = 1

        allowed_categories = INDUSTRY_CATEGORIES.get(
            organization.industry,
            list(PRODUCTS.keys()),
        )

        for customer in customers:

            purchase_count = random_transaction_count()

            for _ in range(purchase_count):

                category = random.choice(
                    allowed_categories
                )

                product = random.choice(
                    PRODUCTS[category]
                )
                quantity = random_quantity()

                unit_price = random_amount(category)

                amount = round(
                    quantity * unit_price,
                    2,
                )

                transaction = Transaction(

                    org_id=organization.id,

                    transaction_code=transaction_code(
                        organization.code,
                        transaction_number,
                    ),

                    customer_id=customer.id,

                    product_name=product,

                    product_category=category,

                    quantity = quantity,

                    amount = amount,

                    payment_method=random_payment_method(),

                    status=random_transaction_status(),

                    transaction_date=random_transaction_date(),

                )

                transactions.append(transaction)

                transaction_number += 1

        self.transaction_repository.create_many(
            transactions
        )

        print(
            f"{organization.name}: "
            f"{len(transactions)} transactions created."
        )

    def generate_demo_data(self):

        self.create_organizations()

        self.create_admin_users()

        for organization in self.organizations.values():

            customers = self.create_customers(
                organization
            )

            self.create_transactions(
                organization,
                customers,
            )