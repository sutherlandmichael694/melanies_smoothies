# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title("Customise your Smoothies :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
  
    """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)



session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
# st.dataframe(data=my_dataframe, use_container_width=True)

# create ingredients list from table column as a multiselect

ingredients_list = st.multiselect( "Choose up to five ingredients", my_dataframe, max_selections=5 )
    
#FOR loop to check for selected fruits, place them into the ingredients_string variable

ingredients_string = ''
if ingredients_list:
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

#using st.write to list the ingredients string from  above

#st.write(ingredients_string)

#Build a SQL Insert Statement & Test It would work in a SQL worksheet to add the ingredients into the ORDERS table

my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order +  """')"""

#st.write(my_insert_stmt)
#st.write('Your Smoothie is ordered,', name_on_order)

#  stops code when written
# st.stop ()


#create button to create a variable called time to insert
time_to_insert = st.button('Submit Order')

# Insert the Order into Snowflake when variable is not null

if time_to_insert:
    session.sql(my_insert_stmt).collect() 
    
    st.success('Your Smoothie is ordered, ' + name_on_order, icon="✅")


