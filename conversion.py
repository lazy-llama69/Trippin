import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Function to fetch exchange rates
def get_conversion( ):
    load_dotenv()
    api_key = os.getenv("EXCHANGE_API_KEY")

    st.title("Currency Converter")

    # Add input fields for user to input the amount and currencies
    amount = st.number_input("Amount to convert", min_value=0.0, value=1.0, format="%.2f")
    base_currency = st.selectbox("Base Currency", ["USD", "EUR", "GBP", "INR", "AUD", "CAD", "JPY"])
    target_currency = st.selectbox("Target Currency", ["USD", "EUR", "GBP", "INR", "AUD", "CAD", "JPY"])


    # When the user clicks the "Convert" button
    if st.button("Convert"):
        conversion_rate = get_exchange_rate(api_key, base_currency, target_currency)
        if conversion_rate:
            converted_amount = amount * conversion_rate
            st.write(f"{amount} {base_currency} is equal to {converted_amount:.2f} {target_currency}.")
        else:
            st.write(f"please try again")

def get_exchange_rate(api_key,base_currency,target_currency):
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


