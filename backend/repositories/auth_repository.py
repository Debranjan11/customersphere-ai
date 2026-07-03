from sqlalchemy.orm import Session

from backend.models.organization import Organization
from backend.models.user import User


class AuthRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_organization(self, organization):
        self.db.add(organization)
        self.db.commit()
        self.db.refresh(organization)
        return organization

    def create_user(self, user):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_email(self, email):
        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def get_organization_by_email(self, email):
        return (
            self.db.query(Organization)
            .filter(Organization.email == email)
            .first()
        )