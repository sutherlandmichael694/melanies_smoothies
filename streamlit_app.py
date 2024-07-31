# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Customise your Smoothies :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
  
    """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)


cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))

# create ingredients list from table column as a multiselect

ingredients_list = st.multiselect( "Choose up to five ingredients", my_dataframe, max_selections=5 )
    
#FOR loop to check for selected fruits, place them into the ingredients_string variable

ingredients_string = ''
if ingredients_list:
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader (fruit_chosen + ' Nutrional Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width = True)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order +  """')"""

#create button to create a variable called time to insert
time_to_insert = st.button('Submit Order')

# Insert the Order into Snowflake when variable is not null

if time_to_insert:
    session.sql(my_insert_stmt).collect() 
    
    st.success('Your Smoothie is ordered, ' + name_on_order, icon="✅")

# new section to imprto fruityvice nutrition information



