

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import firebase
from firebase_key import the_class


firebaseConfig = the_class.firebaseConfig
app = firebase.initialize_app(firebaseConfig)
db = app.firestore()


def get_scorad_arrays():
    uid = st.session_state.user["localId"]
    output = db.collection("scorad").where("uid", "==", uid).get()

    temp_list = []
    temp_list_2 = []

    for i in output:
            temp = list(i.values())[0]
            temp_list.append(temp['date'])
            temp_list_2.append(temp['score'])

    return temp_list, temp_list_2


def get_poem_arrays():
    uid = st.session_state.user["localId"]
    output = db.collection("POEM").where("uid", "==", uid).get()

    temp_list = []
    temp_list_2 = []

    for i in output:
            temp = list(i.values())[0]
            temp_list.append(temp['date'])
            temp_list_2.append(temp['score'])

    return temp_list, temp_list_2




if 'user' not in st.session_state:
    st.session_state.user = ''


if st.session_state.user == '':
    st.warning("Please log in to continue")
    
else:
    st.title('SCORAD Chart')
    date_array , score_array = get_scorad_arrays()
    # Sample data (replace with your actual data)
    data = {
        #"Date": pd.to_datetime(["2024-06-20", "2024-06-27", "2024-07-04", "2024-07-11", "2024-06-24"]),
     
        "Date": pd.to_datetime(date_array),
        #"Score": [80, 75, 90, 85, 65]
        "Score": score_array
    }

    df = pd.DataFrame(data)
    df = df.sort_values(by='Date')

    # Title and chart configuration

    plt.figure(figsize=(10, 6))


    # Plot the line chart
    plt.plot(df["Date"], df["Score"], marker='o', linestyle='-')  # Plot date vs score
    plt.xlabel("Date")
    plt.ylabel("Score")
    plt.title("Score Trend Across Days")
    plt.grid(True)

    plt.xticks(rotation = 'vertical')

    # Display the chart
    st.pyplot(plt)

    #-------------------------------------
    st.title('POEM Chart')
    date_array , score_array = get_poem_arrays()
   
    # Sample data (replace with your actual data)
    data = {
        #"Date": pd.to_datetime(["2024-06-20", "2024-06-27", "2024-07-04", "2024-07-11", "2024-06-24"]),
     
        "Date": pd.to_datetime(date_array),
        #"Score": [80, 75, 90, 85, 65]
        "Score": score_array
    }

    df = pd.DataFrame(data)
    df = df.sort_values(by='Date')

    # Title and chart configuration

    plt.figure(figsize=(10, 6))


    # Plot the line chart
    plt.plot(df["Date"], df["Score"], marker='o', linestyle='-')  # Plot date vs score
    plt.xlabel("Date")
    plt.ylabel("Score")
    plt.title("Score Trend Across Days")
    plt.grid(True)

    plt.xticks(rotation = 'vertical')

    # Display the chart
    st.pyplot(plt)

