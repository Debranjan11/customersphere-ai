from fastapi import HTTPException, status

from backend.models.customer import Customer
from backend.repositories.customer_repository import CustomerRepository


class CustomerService:

    def __init__(self, db):
        self.repository = CustomerRepository(db)


    def generate_customer_code(self, org_id: int):

        last_customer = self.repository.get_last_customer(org_id)

        if last_customer is None:
            customer_number = 1
        else:
            last_code = last_customer.customer_code

            customer_number = int(
                last_code.split("-")[-1]
            ) + 1

        return f"ORG{org_id:03d}-CUST-{customer_number:06d}"
    
    #create customer
    def create_customer(self, request, org_id):

        existing = self.repository.get_by_email(
        request.email,
        org_id,
        )

        if existing:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer email already exists",
        )

        customer = Customer(
            org_id=org_id,
            customer_code=self.generate_customer_code(org_id),
            name=request.name,
            email=request.email,
            phone=request.phone,
            gender=request.gender,
            age=request.age,
            city=request.city,
            state=request.state,
            country=request.country,
            postal_code=request.postal_code,
        )

        return self.repository.create(customer)
    
    #get all customers
    def get_all_customers(
        self,
        org_id,
        page,
        page_size,
        keyword,
        city,
        state,
        is_active,
        sort_by,
        sort_order,
    ):
        return self.repository.get_all_by_org(
            org_id=org_id,
            page=page,
            page_size=page_size,
            keyword=keyword,
            city=city,
            state=state,
            is_active=is_active,
            sort_by=sort_by,
            sort_order=sort_order,
        )
            
    #get customer
    def get_customer(self, customer_id, org_id):

        customer = self.repository.get_by_id(
            customer_id,
            org_id,
        )

        if customer is None:

            raise HTTPException(
                status_code=404,
                detail="Customer not found",
            )

        return customer
    
    #update customer
    def update_customer(
        self,
        customer_id,
        request,
        org_id,
    ):
        existing = self.repository.get_by_email_excluding_customer(
        request.email,
        org_id,
        customer_id,
        )

        if existing:
            raise HTTPException(
            status_code=400,
            detail="Customer email already exists",
            )

        customer = self.get_customer(
            customer_id,
            org_id,
        )

        customer.name = request.name
        customer.email = request.email
        customer.phone = request.phone
        customer.gender = request.gender
        customer.age = request.age
        customer.city = request.city
        customer.state = request.state
        customer.country = request.country
        customer.postal_code = request.postal_code

        return self.repository.update(customer)
    
    #soft delete
    def delete_customer(
        self,
        customer_id,
        org_id,
    ):

        customer = self.get_customer(
            customer_id,
            org_id,
        )

        self.repository.soft_delete(customer)

        return {
            "message": "Customer deleted successfully"
        }
    
    #search customer
    def search_customers(
        self,
        keyword,
        org_id,
    ):

        return self.repository.search(
            org_id,
            keyword,
        )