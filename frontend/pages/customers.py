import streamlit as st

from services.customer_service import (
    customer_service,
)


# ============================================
# Helper Functions
# ============================================

def load_customers(
    token,
    page,
    page_size,
    keyword,
):
    with st.spinner("Loading customers..."):
        response = customer_service.get_customers(
            token=token,
            page=page,
            page_size=page_size,
            keyword=keyword,
        )

    if response.status_code != 200:

        st.error("Unable to load customers.")

        return None

    return response.json()


def display_customer_table(customers):

    if not customers:

        st.info("No customers found.")

        return

    table = []

    for customer in customers:

        table.append(
            {
                "Code": customer["customer_code"],
                "Name": customer["name"],
                "Email": customer["email"],
                "Phone": customer["phone"],
                "City": customer["city"],
                "State": customer["state"],
                "Country": customer["country"],
                "Status": (
                    "Active"
                    if customer["is_active"]
                    else "Inactive"
                ),
            }
        )

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True,
    )


# ============================================
# Main Render Function
# ============================================

def render():

    st.title("👥 Customer Management")

    token = st.session_state.access_token

    st.divider()

    col1, col2 = st.columns([3, 1])

    with col1:

        keyword = st.text_input(
            "🔍 Search Customer",
            placeholder="Search by name, email, phone...",
        )

    with col2:

        page_size = st.selectbox(
            "Page Size",
            [
                5,
                10,
                20,
                50,
            ],
            index=1,
        )

    page = st.number_input(
        "Page",
        min_value=1,
        value=1,
        step=1,
    )

    data = load_customers(
        token,
        page,
        page_size,
        keyword,
    )

    if data is None:

        return

    customers = data["customers"]

    total = data["total"]

    st.caption(
        f"Total Customers : {total}"
    )

    st.divider()

    display_customer_table(
        customers
    )

    st.divider()

        # ============================================
    # Add Customer
    # ============================================

    with st.expander("➕ Add Customer"):

        with st.form("add_customer_form"):

            col1, col2 = st.columns(2)

            with col1:

                name = st.text_input("Name")

                email = st.text_input("Email")

                phone = st.text_input("Phone")

                gender = st.selectbox(
                    "Gender",
                    [
                        "Male",
                        "Female",
                        "Other",
                    ],
                )

                age = st.number_input(
                    "Age",
                    min_value=1,
                    max_value=120,
                    value=18,
                )

            with col2:

                city = st.text_input("City")

                state = st.text_input("State")

                country = st.text_input("Country")

                postal_code = st.text_input(
                    "Postal Code"
                )

            submitted = st.form_submit_button(
                "Create Customer"
            )

            if submitted:

                payload = {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "gender": gender,
                    "age": age,
                    "city": city,
                    "state": state,
                    "country": country,
                    "postal_code": postal_code,
                }
                with st.spinner("Creating customer..."):
                    response = customer_service.create_customer(
                        token,
                        payload,
                    )

                if response.status_code == 201:

                    st.success(
                        "Customer created successfully."
                    )

                    st.rerun()

                else:

                    st.error(response.text)

    st.divider()

    # ============================================
    # Edit Customer
    # ============================================

    if customers:

        customer_options = {
            f"{customer['customer_code']} - {customer['name']}": customer
            for customer in customers
        }

        selected_key = st.selectbox(
            "Select Customer to Edit",
            list(customer_options.keys()),
        )

        selected_customer = customer_options[selected_key]

        with st.expander("✏ Edit Customer"):

            with st.form("edit_customer_form"):

                col1, col2 = st.columns(2)

                with col1:

                    edit_name = st.text_input(
                        "Name",
                        value=selected_customer["name"],
                    )

                    edit_email = st.text_input(
                        "Email",
                        value=selected_customer["email"],
                    )

                    edit_phone = st.text_input(
                        "Phone",
                        value=selected_customer["phone"] or "",
                    )

                    edit_gender = st.selectbox(
                        "Gender",
                        [
                            "Male",
                            "Female",
                            "Other",
                        ],
                        index=[
                            "Male",
                            "Female",
                            "Other",
                        ].index(
                            selected_customer["gender"]
                            if selected_customer["gender"] in [
                                "Male",
                                "Female",
                                "Other",
                            ]
                            else "Other"
                        ),
                    )

                    edit_age = st.number_input(
                        "Age",
                        min_value=1,
                        max_value=120,
                        value=selected_customer["age"]
                        if selected_customer["age"]
                        else 18,
                    )

                with col2:

                    edit_city = st.text_input(
                        "City",
                        value=selected_customer["city"] or "",
                    )

                    edit_state = st.text_input(
                        "State",
                        value=selected_customer["state"] or "",
                    )

                    edit_country = st.text_input(
                        "Country",
                        value=selected_customer["country"] or "",
                    )

                    edit_postal_code = st.text_input(
                        "Postal Code",
                        value=selected_customer["postal_code"] or "",
                    )

                update = st.form_submit_button(
                    "Update Customer"
                )

                if update:

                    payload = {
                        "name": edit_name,
                        "email": edit_email,
                        "phone": edit_phone,
                        "gender": edit_gender,
                        "age": edit_age,
                        "city": edit_city,
                        "state": edit_state,
                        "country": edit_country,
                        "postal_code": edit_postal_code,
                    }
                    with st.spinner("Updating customer..."):
                        response = customer_service.update_customer(
                            token,
                            selected_customer["id"],
                            payload,
                        )

                    if response.status_code == 200:

                        st.success(
                            "Customer updated successfully."
                        )

                        st.rerun()

                    else:

                        st.error(response.text)

    st.divider()

        # ============================================
    # Delete Customer
    # ============================================

    if customers:

        st.subheader("🗑 Delete Customer")

        delete_customer = st.selectbox(
            "Select Customer",
            list(customer_options.keys()),
            key="delete_customer",
        )

        delete_selected = customer_options[
            delete_customer
        ]

        st.warning(
            f"You are about to delete "
            f"{delete_selected['name']}."
        )

        if st.button(
            "Delete Customer",
            type="primary",
        ):
            with st.spinner("Deleting customer..."):
                response = customer_service.delete_customer(
                    token,
                    delete_selected["id"],
                )

            if response.status_code == 200:

                st.success(
                    "Customer deleted successfully."
                )

                st.rerun()

            else:

                st.error(response.text)

    st.divider()

    # ============================================
    # Footer Information
    # ============================================

    st.caption(
        f"Showing {len(customers)} customer(s) "
        f"out of {total}"
    )