import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Function to fetch exchange rates
def get_conversion():
    load_dotenv()
    api_key = os.getenv("EXCHANGE_API_KEY")

    st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1rem !important; /* Adjust the top padding */
            padding-left: 6rem;
            padding-right: 6rem;
        }
    </style>
    """,
    unsafe_allow_html=True
    )

    # Define currency options with full names
    currency_options = {
        "USD (United States Dollar)": "USD",
        "EUR (Euro)": "EUR",
        "GBP (British Pound Sterling)": "GBP",
        "INR (Indian Rupee)": "INR",
        "AUD (Australian Dollar)": "AUD",
        "CAD (Canadian Dollar)": "CAD",
        "JPY (Japanese Yen)": "JPY"
    }

    st.title("Currency Converter")

    # Input fields with modifications
    amount = st.number_input("Amount to convert", min_value=0.0, value=1.0, format="%.2f", step=1.0)
    base_currency_desc = st.selectbox("Base Currency", list(currency_options.keys()))
    base_currency = currency_options[base_currency_desc]
    target_currency_desc = st.selectbox("Target Currency", list(currency_options.keys()))
    target_currency = currency_options[target_currency_desc]

    # When the user clicks the "Convert" button
    if st.button("Convert",type="primary"):
        conversion_rate = get_exchange_rate(api_key, base_currency, target_currency)
        if conversion_rate:
            converted_amount = amount * conversion_rate
            st.write(f"{amount} {base_currency} is equal to {converted_amount:.2f} {target_currency}.")
        else:
            st.write("please try again")

def get_exchange_rate(api_key, base_currency, target_currency):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200 and data['result'] == 'success':
        conversion_rate = data['conversion_rates'].get(target_currency)
        if conversion_rate:
            return conversion_rate
        else:
            st.error(f"Could not find conversion rate for {target_currency}.")
    else:
        st.error("Error fetching data from ExchangeRate-API.")

    return None