from sqlalchemy import asc, desc, or_

from backend.models.customer import Customer
from backend.repositories.base_repository import BaseRepository


class CustomerRepository(BaseRepository):

    def create(self, customer: Customer):
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def get_by_id(self, customer_id: int, org_id: int):
        return (
            self.db.query(Customer)
            .filter(
                Customer.id == customer_id,
                Customer.org_id == org_id,
                Customer.is_active == True,
            )
            .first()
        )
    def get_by_email(self, email: str, org_id: int):
        return (
        self.db.query(Customer)
        .filter(
            Customer.email == email,
            Customer.org_id == org_id,
            Customer.is_active == True,
        )
        .first()
    )
    def get_by_email_excluding_customer(
    self,
    email: str,
    org_id: int,
    customer_id: int,
    ):
        return (
            self.db.query(Customer)
            .filter(
                Customer.email == email,
                Customer.org_id == org_id,
                Customer.id != customer_id,
                Customer.is_active == True,
        )
        .first()
    )

    def get_all_by_org(
        self,
        org_id: int,
        page: int = 1,
        page_size: int = 10,
        keyword: str | None = None,
        city: str | None = None,
        state: str | None = None,
        is_active: bool = True,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ):

        query = self.db.query(Customer).filter(
            Customer.org_id == org_id,
            Customer.is_active == is_active,
        )

        # Keyword Search
        if keyword:
            query = query.filter(
                or_(
                    Customer.name.ilike(f"%{keyword}%"),
                    Customer.email.ilike(f"%{keyword}%"),
                    Customer.phone.ilike(f"%{keyword}%"),
                    Customer.customer_code.ilike(f"%{keyword}%"),
                )
            )

        # City Filter
        if city:
            query = query.filter(Customer.city == city)

        # State Filter
        if state:
            query = query.filter(Customer.state == state)

        # Sorting
        sort_column = getattr(Customer, sort_by, Customer.created_at)

        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))

        total = query.count()

        customers = (
            query.offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "customers": customers,
        }

    def update(self, customer: Customer):
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def soft_delete(self, customer: Customer):
        customer.is_active = False
        self.db.commit()

    def search(self, org_id: int, keyword: str):
        return (
            self.db.query(Customer)
            .filter(
                Customer.org_id == org_id,
                Customer.is_active == True,
                or_(
                    Customer.name.ilike(f"%{keyword}%"),
                    Customer.email.ilike(f"%{keyword}%"),
                    Customer.phone.ilike(f"%{keyword}%"),
                    Customer.customer_code.ilike(f"%{keyword}%"),
                ),
            )
            .all()
        )

    def get_last_customer(self, org_id: int):
        return (
            self.db.query(Customer)
            .filter(Customer.org_id == org_id)
            .order_by(Customer.id.desc())
            .first()
        )
    