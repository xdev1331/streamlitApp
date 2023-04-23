import streamlit
import pandas as pd
import requests as rq
#import snowflake.connector


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

# New Section
streamlit.header("Fruityvice Fruit Advice!")

#add user input
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

# use api calls
fruityvice_response = rq.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# comment out this json display
#streamlit.text(fruityvice_response.json())

# write your own comment -what does the next line do? 
# converses joson to table view
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# write your own comment - display the table veiw
streamlit.dataframe(fruityvice_normalized)
