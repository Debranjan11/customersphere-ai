import streamlit as st

from services.transaction_service import (
    transaction_service,
)

from services.customer_service import (
    customer_service,
)


# ============================================
# Helper Functions
# ============================================

def load_transactions(
    token,
    page,
    page_size,
    keyword,
):

    response = transaction_service.get_transactions(
        token=token,
        page=page,
        page_size=page_size,
        keyword=keyword,
    )

    if response.status_code != 200:

        st.error(
            "Unable to load transactions."
        )

        return None

    return response.json()


def display_transaction_table(
    transactions,
):

    if not transactions:

        st.info(
            "No transactions found."
        )

        return

    table = []

    for transaction in transactions:

        table.append(
            {
                "Transaction Code": transaction["transaction_code"],
                "Customer ID": transaction["customer_id"],
                "Product": transaction["product_name"],
                "Category": transaction["product_category"],
                "Quantity": transaction["quantity"],
                "Amount": transaction["amount"],
                "Payment": transaction["payment_method"],
                "Status": transaction["status"],
                "Date": transaction["transaction_date"],
            }
        )

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True,
    )


# ============================================
# Main Page
# ============================================

def render():

    st.title("💳 Transaction Management")

    token = st.session_state.access_token

    st.divider()

    col1, col2 = st.columns([3, 1])

    with col1:

        keyword = st.text_input(
            "🔍 Search Transaction",
            placeholder="Search by product or category...",
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
    with st.spinner("Loading transactions..."):
        data = load_transactions(
            token,
            page,
            page_size,
            keyword,
        )

    if data is None:

        return

    transactions = data["transactions"]

    total = data["total"]

    st.caption(
        f"Total Transactions : {total}"
    )

    st.divider()

    display_transaction_table(
        transactions
    )

    st.divider()

        # ============================================
    # Customer Dropdown
    # ============================================

    customer_options = customer_service.get_customer_dropdown(
        token
    )

    # ============================================
    # Add Transaction
    # ============================================

    with st.expander("➕ Add Transaction"):

        with st.form("add_transaction_form"):

            selected_customer = st.selectbox(
                "Customer",
                customer_options,
                format_func=lambda x: x["label"],
            )

            product_name = st.text_input(
                "Product Name"
            )

            product_category = st.text_input(
                "Product Category"
            )

            quantity = st.number_input(
                "Quantity",
                min_value=1,
                value=1,
            )

            amount = st.number_input(
                "Amount",
                min_value=0.0,
                value=0.0,
                step=1.0,
            )

            payment_method = st.selectbox(
                "Payment Method",
                [
                    "Cash",
                    "UPI",
                    "Credit Card",
                    "Debit Card",
                    "Net Banking",
                ],
            )

            status = st.selectbox(
                "Status",
                [
                    "Completed",
                    "Pending",
                    "Cancelled",
                    "Refunded",
                ],
            )

            submitted = st.form_submit_button(
                "Create Transaction"
            )

            if submitted:

                payload = {

                    "customer_id": selected_customer["id"],

                    "product_name": product_name,

                    "product_category": product_category,

                    "quantity": quantity,

                    "amount": amount,

                    "payment_method": payment_method,

                    "status": status,
                }
                with st.spinner("Creating transaction..."):
                    response = transaction_service.create_transaction(
                        token,
                        payload,
                    )

                if response.status_code == 201:

                    st.success(
                        "Transaction created successfully."
                    )

                    st.rerun()

                else:

                    st.error(response.text)

    st.divider()

    # ============================================
    # Edit Transaction
    # ============================================

    if transactions:

        transaction_options = {

            f"{transaction['transaction_code']} - {transaction['product_name']}":

            transaction

            for transaction in transactions

        }

        selected_key = st.selectbox(

            "Select Transaction",

            list(transaction_options.keys()),

        )

        selected_transaction = transaction_options[
            selected_key
        ]

        current_customer = next(

            (
                customer
                for customer in customer_options
                if customer["id"] == selected_transaction["customer_id"]
            ),

            customer_options[0]

        )

        with st.expander("✏ Edit Transaction"):

            with st.form("edit_transaction_form"):

                edit_customer = st.selectbox(

                    "Customer",

                    customer_options,

                    index=customer_options.index(
                        current_customer
                    ),

                    format_func=lambda x: x["label"],

                )

                edit_product = st.text_input(

                    "Product Name",

                    value=selected_transaction[
                        "product_name"
                    ],

                )

                edit_category = st.text_input(

                    "Product Category",

                    value=selected_transaction[
                        "product_category"
                    ],

                )

                edit_quantity = st.number_input(

                    "Quantity",

                    min_value=1,

                    value=selected_transaction[
                        "quantity"
                    ],

                )

                edit_amount = st.number_input(

                    "Amount",

                    min_value=0.0,

                    value=float(
                        selected_transaction[
                            "amount"
                        ]
                    ),

                )

                edit_payment = st.selectbox(

                    "Payment Method",

                    [
                        "Cash",
                        "UPI",
                        "Credit Card",
                        "Debit Card",
                        "Net Banking",
                    ],

                    index=[
                        "Cash",
                        "UPI",
                        "Credit Card",
                        "Debit Card",
                        "Net Banking",
                    ].index(
                        selected_transaction[
                            "payment_method"
                        ]
                    ),

                )

                edit_status = st.selectbox(

                    "Status",

                    [
                        "Completed",
                        "Pending",
                        "Cancelled",
                        "Refunded",
                    ],

                    index=[
                        "Completed",
                        "Pending",
                        "Cancelled",
                        "Refunded",
                    ].index(
                        selected_transaction[
                            "status"
                        ]
                    ),

                )

                update = st.form_submit_button(
                    "Update Transaction"
                )

                if update:

                    payload = {

                        "customer_id": edit_customer["id"],

                        "product_name": edit_product,

                        "product_category": edit_category,

                        "quantity": edit_quantity,

                        "amount": edit_amount,

                        "payment_method": edit_payment,

                        "status": edit_status,
                    }
                    with st.spinner("Updating transaction..."):
                        response = transaction_service.update_transaction(

                            token,

                            selected_transaction["id"],

                            payload,

                        )

                    if response.status_code == 200:

                        st.success(
                            "Transaction updated successfully."
                        )

                        st.rerun()

                    else:

                        st.error(response.text)

    st.divider()

        # ============================================
    # Delete Transaction
    # ============================================

    if transactions:

        st.subheader("🗑 Delete Transaction")

        delete_transaction = st.selectbox(
            "Select Transaction",
            list(transaction_options.keys()),
            key="delete_transaction",
        )

        delete_selected = transaction_options[
            delete_transaction
        ]

        st.warning(
            f"You are about to delete transaction "
            f"{delete_selected['transaction_code']}."
        )

        if st.button(
            "Delete Transaction",
            type="primary",
        ):
            with st.spinner("Deleting transaction..."):
                response = transaction_service.delete_transaction(
                    token,
                    delete_selected["id"],
                )

            if response.status_code == 200:

                st.success(
                    "Transaction deleted successfully."
                )

                st.rerun()

            else:

                st.error(response.text)

    st.divider()

    # ============================================
    # Dashboard Summary
    # ============================================

    completed = len(
        [
            t
            for t in transactions
            if t["status"] == "Completed"
        ]
    )

    pending = len(
        [
            t
            for t in transactions
            if t["status"] == "Pending"
        ]
    )

    cancelled = len(
        [
            t
            for t in transactions
            if t["status"] == "Cancelled"
        ]
    )

    refunded = len(
        [
            t
            for t in transactions
            if t["status"] == "Refunded"
        ]
    )

    total_amount = sum(
        float(t["amount"])
        for t in transactions
    )

    st.subheader("📈 Transaction Summary")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Total",
        len(transactions),
    )

    col2.metric(
        "Completed",
        completed,
    )

    col3.metric(
        "Pending",
        pending,
    )

    col4.metric(
        "Cancelled",
        cancelled,
    )

    col5.metric(
        "Revenue",
        f"₹ {total_amount:,.2f}",
    )

    st.divider()

    st.caption(
        f"Showing {len(transactions)} transaction(s) "
        f"out of {total}"
    )