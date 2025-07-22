
# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Smoothie Orders:cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Get the active session
cnx = st.connection("snowflake")
session = cnx.session
# Access the fruit options table
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).to_pandas()

# Display the dataframe (optional)
# st.dataframe(data=my_dataframe, use_container_width=True)

# Create a multiselect widget
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', my_dataframe['FRUIT_NAME'].tolist(),max_selections=5
)

import requests
import streamlit as st

if ingredients_list:
    # Join the selected ingredients into a string
    ingredients_string = ', '.join(ingredients_list)

    # Display the selected ingredients
    st.write("Selected ingredients:", ingredients_string)

    # Fetch and display nutrition info for each ingredient
    for fruit in ingredients_list:
        try:
            response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{fruit.lower()}")
            if response.status_code == 200:
                fruit_data = response.json()
                st.subheader(f"Nutrition info for {fruit.capitalize()}:")
                st.dataframe(data=fruit_data, use_container_width=True)
            else:
                st.warning(f"Could not fetch data for {fruit}")
        except Exception as e:
            st.error(f"Error fetching data for {fruit}: {e}")

    # Submit button
    submitted = st.button('Submit')
    if submitted:
        st.success("Your smoothie is ordered!")

        # Create the SQL insert statement
        my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(name_on_order, ingredients)
        VALUES ('{name_on_order}', '{ingredients_string}')
        """

        # Execute the SQL insert statement
        session.sql(my_insert_stmt).collect()

        # Display the SQL insert statement
        st.write("SQL insert statement executed:", my_insert_stmt)



st.stop()

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
