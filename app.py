from typing import Never
import pandas as pd
import plotly.express as px
import streamlit as st
import sqlite3
import plotly.express as px
from PIL import Image







st.set_page_config(
    page_title="Observations tracking",
    page_icon=":bar_chart:",
    layout="wide"
)


     







# Define the expected password
expected_password = "1"

# Add a text input widget for the user to enter the password
password = st.sidebar.text_input("Enter Password:", type="password")

# Check if the entered password matches the expected value
if password == expected_password:
    st.write("Access Granted!")

      
    

    edited_df = 'Business Park.xlsx'
    sheet_name = 'DATA'

    df = pd.read_excel(
        io='Business Park.xlsx',
        engine='openpyxl',
        sheet_name='DATA',
        skiprows=2,
        usecols='B:H',
        nrows=400,
    )

    

    # Display the header and subheader
    st.header("**Emaar Misr**")
    st.subheader("Observations Tracking", anchor="observations-tracking")
    

    

    
    


    # Create a SQLite database
    conn = sqlite3.connect('my_database.db')

    # Store the DataFrame in the database
    df.to_sql('my_table', conn, if_exists='replace', index=False)

    # Create a Streamlit app
    st.title('Tracking Sheet')

     #  Display the editable DataFrame
    edited_df = st.data_editor(df, num_rows="dynamic")

    # When a user clicks a button, save the edited DataFrame back to the database
    try:
        if st.button('Save Changes'):
          edited_df.to_sql('my_table', conn, if_exists='replace', index=False)
          edited_df.to_excel('Business_Park_Edited.xlsx', index=False)
    except Exception as e:
     st.error(f"An error occurred: {e}")



    # Close the connection to the database
    conn.close()

    


    key_1 = 'data_editor1'
    key_2 = 'data_editor2'
    key_3 = 'data_editor3'   



    




    

  

    st.sidebar.header("Select Data")
    data_selection = st.sidebar.radio("Choose Data:", ("Original Data", "Edited Data"))

    if data_selection == "Original Data":
        selected_df = df
    else:
        selected_df = edited_df

    # Assume df contains your data

     # Identify the top 8 most occurring elements for both x-axis and y-axis
    top_x_elements = df['Observation'].value_counts().nlargest(10).index.tolist()
    top_y_elements = df['Building'].value_counts().nlargest(10).index.tolist()

    # Filter your DataFrame to include only those elements
    filtered_df = df[df['Observation'].isin(top_x_elements) & df['Building'].isin(top_y_elements)]
   

     # Create a frequency table of the top 8 buildings
    building_counts = filtered_df['Building'].value_counts().nlargest(8)

     # Create a list of the top 8 buildings
    top_buildings = building_counts.index.tolist()

     # Filter the DataFrame to include only the top 8 buildings
    filtered_df = filtered_df[filtered_df['Building'].isin(top_buildings)]


    # Create the bar chart using Plotly Express with the filtered data
    fig = px.bar(filtered_df, x='Building', y='Observation', title="Top 8 Observations vs Buildings")


    # Show the chart
    st.plotly_chart(fig)

    st.area_chart(
    data=filtered_df,
    x="Building",
    y="Observation",
    )


    image = Image.open('C:\\Users\\dell\\Desktop\\gg\\Main\\Emaar_Properties_logo_PNG2.png')
    st.image(image, width=200)


    st.markdown("---")

else:
    st.error("Invalid Password. Access Denied.")
