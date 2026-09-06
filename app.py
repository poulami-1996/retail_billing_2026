import streamlit as st


# -----------------------------
# Manager offer calculation
# -----------------------------
def manager(offer=0):
    return lambda total_mrp: total_mrp * (100 - offer) / 100


# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Billing System",
    page_icon="🧾",
    layout="centered"
)

st.title("🧾 Billing Management System")


# -----------------------------
# Initialize session variables
# -----------------------------
if "manager_logged_in" not in st.session_state:
    st.session_state.manager_logged_in = False

if "cashier_logged_in" not in st.session_state:
    st.session_state.cashier_logged_in = False

if "billing_formula" not in st.session_state:
    st.session_state.billing_formula = manager()

if "total_mrp" not in st.session_state:
    st.session_state.total_mrp = 0.0

if "items" not in st.session_state:
    st.session_state.items = []


# ============================================================
# MANAGER LOGIN
# ============================================================

st.header("👨‍💼 Manager Login")

if not st.session_state.manager_logged_in:

    userid_login_m = st.text_input(
        "Dear Manager, Enter your userid",
        key="manager_userid"
    )

    password_login_m = st.text_input(
        "Enter your password",
        type="password",
        key="manager_password"
    )

    if st.button("Manager Login"):

        userid_m = "manager@12"
        password_m = "manager@123"

        if userid_m == userid_login_m and password_m == password_login_m:

            st.session_state.manager_logged_in = True

            st.success("Manager login successful!")

            # Offer input
            st.rerun()

        else:
            st.error("User id or password is wrong... try again.")


else:

    st.success("Manager is logged in.")

    offer = st.number_input(
        "Enter today's offer value (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=1.0
    )

    if st.button("Apply Offer"):

        st.session_state.billing_formula = manager(offer)

        st.success(f"Today's offer of {offer:.2f}% has been applied.")


# ============================================================
# CASHIER LOGIN
# ============================================================

st.divider()

st.header("👨‍💼 Cashier Login")

if not st.session_state.cashier_logged_in:

    userid_login_cashier = st.text_input(
        "Dear Cashier, Enter your userid",
        key="cashier_userid"
    )

    password_login_cashier = st.text_input(
        "Enter your password",
        type="password",
        key="cashier_password"
    )

    if st.button("Cashier Login"):

        userid_cashier = "cashier@12"
        password_cashier = "cashier@123"

        if (
            userid_cashier == userid_login_cashier
            and password_cashier == password_login_cashier
        ):

            st.session_state.cashier_logged_in = True

            st.success("Billing can be started now.")

            st.rerun()

        else:

            st.error(
                "Wrong userid or password, "
                "try again, billing cannot be started."
            )


# ============================================================
# BILLING SECTION
# ============================================================

if st.session_state.cashier_logged_in:

    st.divider()

    st.header("🛒 Billing")

    # Product entry
    price = st.number_input(
        "Enter price of the item",
        min_value=0.0,
        value=0.0,
        step=1.0,
        key="price"
    )

    quantity = st.number_input(
        "Enter quantity of above item",
        min_value=1,
        value=1,
        step=1,
        key="quantity"
    )

    if st.button("Add Item"):

        total_for_a_product = price * quantity

        st.session_state.total_mrp += total_for_a_product

        st.session_state.items.append(
            {
                "Price": price,
                "Quantity": quantity,
                "Total": total_for_a_product
            }
        )

        st.success(
            f"Item added. Total for this product: "
            f"₹{total_for_a_product:.2f}"
        )

        st.rerun()


    # -----------------------------
    # Display current bill
    # -----------------------------

    if st.session_state.items:

        st.subheader("📋 Current Bill")

        for i, item in enumerate(st.session_state.items, start=1):

            st.write(
                f"**{i}.** "
                f"Price: ₹{item['Price']:.2f} × "
                f"Quantity: {item['Quantity']} = "
                f"₹{item['Total']:.2f}"
            )

        st.divider()

        st.write(
            f"### Total MRP: ₹{st.session_state.total_mrp:.2f}"
        )


    # -----------------------------
    # Finish billing
    # -----------------------------

    if st.button("🧾 Finish Billing"):

        total_amount_payable_c = st.session_state.billing_formula(
            st.session_state.total_mrp
        )

        st.success(
            f"### Total Amount Payable by Customer: "
            f"₹{total_amount_payable_c:.2f}"
        )

        discount = (
            st.session_state.total_mrp
            - total_amount_payable_c
        )

        st.info(
            f"Discount: ₹{discount:.2f}"
        )


    # -----------------------------
    # New bill
    # -----------------------------

    if st.button("🔄 Start New Bill"):

        st.session_state.total_mrp = 0.0
        st.session_state.items = []

        st.success("New bill started.")

        st.rerun()