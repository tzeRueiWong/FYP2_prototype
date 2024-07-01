import streamlit as st
import firebase
import datetime
import pandas as pd

from firebase_key import the_class


firebaseConfig = the_class.firebaseConfig
app = firebase.initialize_app(firebaseConfig)
db = app.firestore()

def is_same_week(date_1, date_2):
    
    # assuming both dates are date objects
    # assuming date_1 < date_2

    day_dif = (date_2 - date_1).days

    if day_dif < 7 and (date_2.weekday() - date_1.weekday()) >= 0:
        return True
    
    # else
    return False

def get_latest_entry_date():
    
    uid = st.session_state.user['localId']

    query = db.collection("POEM").where("uid", "==", uid).get()

    if len(query) == 0: # if no entry for current user, return null
        return None


    date_list = []

    for i in query:
        temp = list(i.values())[0]["date"]
        date_list.append(temp)


    df = pd.DataFrame({'Dates': date_list}) # init panda object
    df['Dates'] = pd.to_datetime(df['Dates']) # convert date string to date obj
    max_date = df['Dates'].max().date() # return max date, date is obj

    return max_date # date is object


def submit_poem(the_dict):
    score= 0

    for i in the_dict.values():
        if i == 0:
            score += 0
        elif i == 1 or i ==2:
            score +=1
        elif i == 3 or i==4:
            score+=2
        elif i==5 or i==6:
            score+=3
        else:
            score+=4
    
    if score == 0: # getting value of 0 from firebase raises Python's doubleValue error
        score = None

    uid = st.session_state.user['localId']

    today = str(datetime.date.today())

    latest_date = get_latest_entry_date()

    
    if latest_date != None and is_same_week(latest_date, datetime.date.today()):
        
        query = db.collection("POEM").where("uid", "==", uid).where("date", "==", str(latest_date)).get()

        row_dict = query[0]

        data = {"date":today, "score":score, "uid":uid}

        db.collection("POEM").document(list(row_dict.keys())[0]).set(data)

    else:
        data = {"uid":uid, "score":score, "date": today}
        db.collection("POEM").add(data)




if 'user' not in st.session_state:
    st.session_state.user = ''


if st.session_state.user == '':
    st.warning("Please log in to continue")
    
else:

    st.title("Quality Of Life (POEM Test)")

    tab_1, tab_2 = st.tabs(["Test", "History"])

    with tab_1:

        with st.form("POEM form", clear_on_submit=True):

            the_dict = {}

            the_dict['itchy'] = st.slider(
                'Over the last week, on how many days has your skin been itchy due to eczema?',
                min_value = 0, max_value=7,step=1)

            the_dict['sleep'] = st.slider(
            'Over the last week, on how many night has your sleep been disturbed due to eczema?',
            min_value = 0, max_value=7,step=1)

            the_dict['bleed'] = st.slider(
                'Over the last week, on how many days has your skin been bleeding due to eczema?',
                min_value = 0, max_value=7,step=1)

            the_dict['oozing'] = st.slider(
                'Over the last week, on how many days has your skin been oozing clear fluid due to eczema?',
                min_value = 0, max_value=7,step=1)

            the_dict['crack'] = st.slider(
            'Over the last week, on how many days has your skin been cracked due to eczema?',
            min_value = 0, max_value=7,step=1)

            the_dict['flaking'] = st.slider(
            'Over the last week, on how many days has your skin been flaking off due to eczema?',
            min_value = 0, max_value=7,step=1)

            the_dict['dry'] = st.slider(
            'Over the last week, on how many days has your skin felt dry/rough off due to eczema?',
            min_value = 0, max_value=7,step=1)


            if st.form_submit_button("Submit"):
                submit_poem(the_dict)
                st.rerun()

    with tab_2:

        with st.container(border = True):

            st.subheader("Past Records")

            uid = st.session_state.user["localId"]
            query = db.collection("POEM").where("uid", "==", uid).get()
            
            temp_list = []

            for i in query:
                temp = list(i.values())[0]
                temp_list.append(temp)

            df = pd.DataFrame(data = temp_list) 
            df = df.drop(columns = ["uid"])
            df = df.loc[:,['date','score']]

            st.dataframe(df, use_container_width=True,)
