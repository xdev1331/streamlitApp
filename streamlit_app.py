import streamlit
import pandas as pd
import requests as rq
import snowflake.connector
from urllib.error import URLError


streamlit.title("My parents New Healthy Diner")

streamlit.header('Beakfast Favorites')
streamlit.text(' 🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text(' 🐔 Hard-Boiled Free-Range Egg')
streamlit.text(' 🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

asw_S3_dabw = "https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/"
filename = "fruit_macros.txt"

filepathname = asw_S3_dabw + filename

my_fruit_list = pd.read_csv(filepathname)

#set the index by fruit name instead of id
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
# set the select fruit variable
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

# locate the selected in the myfruit list
fruits_to_show = my_fruit_list.loc[fruits_selected]


# Display the table on the page.
#only display the selected fruit
streamlit.dataframe(fruits_to_show)



#function to api call for getting fruit choice
def get_fruityvice_data(this_fruit_choice):
    # use api calls
    fruityvice_response = rq.get("https://fruityvice.com/api/fruit/" + fruit_choice)

    # write your own comment -what does the next line do? 
    # converses joson to table view
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    # write your own comment - display the table veiw
    return fruityvice_normalized



#rewrite the fruityvice api response
streamlit.header('Fruitvice Fruit Advice!')

try:
    fruit_choice = streamlit.text_input("What fruit would you like information about?")
    if not fruit_choice:
      streamlit.error("Please select a fruit to get information")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
        
except URLError as e:
   streamlit.error()





# New Section
##streamlit.header("Fruityvice Fruit Advice!")

#add user input
##fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
##streamlit.write('The user entered ', fruit_choice)

# use api calls
##fruityvice_response = rq.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# comment out this json display
#streamlit.text(fruityvice_response.json())

# write your own comment -what does the next line do? 
# converses joson to table view
##fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# write your own comment - display the table veiw
##streamlit.dataframe(fruityvice_normalized)



#re-org the snowflake connector section
streamlit.header("The fruit load list contains:")

#snowflake related functions
def get_fruit_load_list(snow_connector):
    with snow_connector.cursor() as my_cur:
        my_cur.execute("select * from PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
        return my_cur.fetchall()
 
#add the button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list(my_cnx)
    streamlit.dataframe(my_data_rows)


#create new function for inserting row into snowflake
# All the end user to add fruit ot the fruit load list
def insert_row_snowflake(new_fruit ,snow_connector):
    with snow_connector.cursor() as my_cur:
        my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values('from streamlit');")
        return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input("What fruit would you like to add?")
if streamlit.button('Add a fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_insert_row_snowflake = insert_row_snowflake(add_my_fruit, my_cnx)
    streamlit.text(back_from_insert_row_snowflake)
    
    
    
    
streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall()
streamlit.header("Fruit Load list:")
streamlit.dataframe(my_data_rows)


#add user input
add_fruit = streamlit.text_input('What fruit would you like add?','Jackfruit')
streamlit.write('Thank you for adding ', add_fruit)

#add the fruit to list
my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values('from streamlit');")
