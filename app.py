import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="GST Rate Finder", page_icon="🧾", layout="centered")

DATA_FILE = Path(__file__).parent / "products.csv"
REQUIRED_COLUMNS = [
    "product_name", "product_price", "gst_rate", "hsn_code",
    "gst_applicability", "official_source"
]

def load_products():
    """Load the local product database safely."""
    try:
        if not DATA_FILE.exists():
            return pd.DataFrame(columns=REQUIRED_COLUMNS)
        df = pd.read_csv(DATA_FILE)
        for col in REQUIRED_COLUMNS:
            if col not in df.columns:
                df[col] = ""
        return df[REQUIRED_COLUMNS].fillna("")
    except Exception as exc:
        st.error(f"Could not read products.csv: {exc}")
        return pd.DataFrame(columns=REQUIRED_COLUMNS)

def clean_text(value):
    return str(value).strip()

def money(value):
    return f"₹{value:,.2f}"

st.title("GST RATE FINDER")
st.write("Find product GST information and calculate the price including GST.")
st.info(
    "GST rates and HSN classifications must be checked against the latest "
    "official CBIC/GST notifications. The CSV is your editable product database."
)

products = load_products()

with st.form("search_form"):
    product_query = st.text_input("Enter product name", placeholder="e.g. laptop")
    col_search, col_clear = st.columns(2)
    search_clicked = col_search.form_submit_button("Search", use_container_width=True)
    clear_clicked = col_clear.form_submit_button("Clear", use_container_width=True)

if clear_clicked:
    st.rerun()

if search_clicked:
    if not product_query.strip():
        st.warning("Please enter a product name.")
    elif products.empty:
        st.error("Product not available. The product database is empty. Add products to products.csv and try again.")
    else:
        matches = products[
            products["product_name"].astype(str).str.contains(
                product_query.strip(), case=False, na=False, regex=False
            )
        ]

        if matches.empty:
            st.error("Product not available.")
        else:
            selected = matches.iloc[0]
            st.subheader("Product Information")
            st.write(f"**Name of the product:** {clean_text(selected['product_name'])}")
            st.write(f"**Product price:** {clean_text(selected['product_price']) or 'Not provided'}")
            st.write(f"**GST rate:** {clean_text(selected['gst_rate']) or 'Not provided'}")
            st.write(f"**GST applicability status:** {clean_text(selected['gst_applicability']) or 'Not provided'}")
            st.write(f"**HSN code:** {clean_text(selected['hsn_code']) or 'Not provided'}")
            source = clean_text(selected["official_source"])
            if source:
                st.markdown(f"**Official source:** [{source}]({source})")
            else:
                st.write("**Official source:** Not provided")

            try:
                price = float(str(selected["product_price"]).replace(",", "").replace("₹", "").strip())
                rate = float(str(selected["gst_rate"]).replace("%", "").strip())
                if price < 0 or rate < 0:
                    raise ValueError("Price and GST rate must be non-negative.")
            except (ValueError, TypeError):
                st.warning(
                    "A valid numeric product_price and gst_rate are required in products.csv "
                    "to calculate the final price."
                )
            else:
                st.subheader("Transaction Details")
                states = [
                    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
                    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
                    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya",
                    "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim",
                    "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand",
                    "West Bengal", "Andaman and Nicobar Islands", "Chandigarh",
                    "Dadra and Nagar Haveli and Daman and Diu", "Delhi", "Jammu and Kashmir",
                    "Ladakh", "Lakshadweep", "Puducherry"
                ]
                col_from, col_to = st.columns(2)
                supplier_state = col_from.selectbox("Supplier state", states, key="supplier_state")
                buyer_state = col_to.selectbox("Buyer state", states, key="buyer_state")

                gst_amount = price * rate / 100
                final_price = price + gst_amount

                if supplier_state == buyer_state:
                    st.success("Transaction type: Intra-state")
                    st.write(f"**CGST ({rate/2:g}%):** {money(gst_amount / 2)}")
                    st.write(f"**SGST ({rate/2:g}%):** {money(gst_amount / 2)}")
                else:
                    st.success("Transaction type: Inter-state")
                    st.write(f"**IGST ({rate:g}%):** {money(gst_amount)}")

                st.divider()
                st.metric("Final price including GST", money(final_price))

st.caption("For educational and informational use. Confirm classification and applicable rates with official GST sources before relying on them.")
