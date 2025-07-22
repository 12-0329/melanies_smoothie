# Import required packages
import streamlit as st
import pandas as pd
import requests
from snowflake.snowpark.functions import col

# App title and instructions
st.title(":cup_with_straw: Customize Smoothie Orders :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie")

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Query fruit options from Snowflake
fruit_df = session.table("smoothies.public.fruit_options").select(
    col("FRUIT_NAME"), col("SEARCH_ON")
)
pd_df = fruit_df.to_pandas()

# Optional: Show available fruits
st.subheader("Available Fruits")
st.dataframe(pd_df, use_container_width=True)

# Form for smoothie customization
with st.form("smoothie_form"):
    name_on_order = st.text_input("Name on Smoothie:")
    ingredients_list = st.multiselect(
        "Choose up to 5 ingredients:",
        pd_df["FRUIT_NAME"].tolist(),
        max_selections=5
    )
    submitted = st.form_submit_button("Submit")

# Handle form submission
if submitted:
    st.write("The name on your Smoothie will be:", name_on_order)

    if ingredients_list:
        for fruit in ingredients_list:
            search_on = pd_df.loc[pd_df["FRUIT_NAME"] == fruit, "SEARCH_ON"].iloc[0]
            st.subheader(f"{fruit} Nutrition Information")

            # Fetch nutrition info from external API
            api_url = f"https://my.smoothiefroot.com/api/fruit/{search_on}"
            response = requests.get(api_url)

            if response.status_code == 200:
                st.dataframe(response.json(), use_container_width=True)
            else:
                st.error(f"Could not fetch data for {fruit}.")
    else:
        st.warning("Please select at least one ingredient.")
