from backend.models.customer import Customer

from backend.repositories.base_repository import BaseRepository


class CustomerRepository(BaseRepository):

    def get_all_by_org(self, org_id):

        return (
            self.db.query(Customer)
            .filter(Customer.org_id == org_id)
            .all()
        )

    def get_by_id(self, customer_id, org_id):

        return (
            self.db.query(Customer)
            .filter(
                Customer.id == customer_id,
                Customer.org_id == org_id,
            )
            .first()
        )