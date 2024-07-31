# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

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

my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'), col('search_on'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

# convert the snowpark dataframe to a pandas dataframe so we can use the LOC function
pd_df=my_dataframe.to_pandas()
# st.dataframe(pd_df)


# create ingredients list from table column as a multiselect

ingredients_list = st.multiselect( "Choose up to five ingredients", my_dataframe, max_selections=5 )
    
#FOR loop to check for selected fruits, place them into the ingredients_string variable

ingredients_string = ''
if ingredients_list:
        
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader (fruit_chosen + ' Nutrional Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width = True)
        # st.write("https://fruityvice.com/api/fruit/" + search_on)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order +  """')"""

#create button to create a variable called time to insert
time_to_insert = st.button('Submit Order')

# Insert the Order into Snowflake when variable is not null

if time_to_insert:
    session.sql(my_insert_stmt).collect() 
    
    st.success('Your Smoothie is ordered, ' + name_on_order, icon="✅")

# new section to imprto fruityvice nutrition information



