import streamlit as st
import firebase
import datetime
import pandas as pd

from firebase_key import the_class


firebaseConfig = the_class.firebaseConfig
app = firebase.initialize_app(firebaseConfig)
db = app.firestore()


def get_score_from_date(date):

    #assuming date is date object

    uid = st.session_state.user["localId"]

    query = db.collection("scorad").where("uid", "==", uid).where("date", "==", str(date) ).get()


    target_score = list(query[0].values())[0]["score"]

    if target_score == None:
        target_score = 0

    return target_score  


def get_latest_entry_date():
    
    uid = st.session_state.user['localId']

    query = db.collection("scorad").where("uid", "==", uid).get()

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


def is_same_week(date_1, date_2):
    
    # assuming both dates are date objects
    # assuming date_1 < date_2

    day_dif = (date_2 - date_1).days

    if day_dif < 7 and (date_2.weekday() - date_1.weekday()) >= 0:
        return True
    
    # else
    return False

def submit_scorad(scorad_dict):
    extent = 0
    intensity = 0
    sub_symptoms = 0

    for i in scorad_dict["extent"].values():
        extent += i

    
    for i in scorad_dict["intensity"].values():
        intensity += i

    
    for i in scorad_dict["sub_symp"].values():
        sub_symptoms += i


    score = extent / 5 + 7 * intensity / 2 + sub_symptoms

    if score == 0: # getting value of 0 from firebase raises Python's doubleValue error
        score = None

    uid = st.session_state.user['localId']

    today = str(datetime.date.today())

    latest_date = get_latest_entry_date()

    
    if latest_date != None and is_same_week(latest_date, datetime.date.today()):
        
        query = db.collection("scorad").where("uid", "==", uid).where("date", "==", str(latest_date)).get()

        row_dict = query[0]

        data = {"date":today, "score":score, "uid":uid}

        db.collection("scorad").document(list(row_dict.keys())[0]).set(data)

    else:
        data = {"uid":uid, "score":score, "date": today}
        db.collection("scorad").add(data)


if 'user' not in st.session_state:
    st.session_state.user = ''


if st.session_state.user == '':
    st.warning("Please log in to continue")
    
else:
    st.title("SCORAD Test")

    tab_1, tab_2 = st.tabs(["Test", "History"])

    with tab_1:

        latest_date = get_latest_entry_date()
        
        if latest_date != None and is_same_week(latest_date, datetime.date.today()):
            
            latest_score = get_score_from_date(latest_date)

            st.subheader("Last record this week is on " + str(latest_date) + ", Score: " + str(latest_score))
            st.text("you have already submitted your scorad score this week")
            
            st.write(f":red[submitting another scorad test will overwrite the score this week]")

        with st.form("Scorad form", clear_on_submit=True):

            with st.expander("Extent"):

                extent_dict = {}

                st.markdown("**On a scale of 0-9, select how much area the Eczema is covering the following body parts. The higher the number, the more skin area coverage**")

                extent_dict["head_neck"] = st.slider(
                    'Head and neck',
                    min_value = 0, max_value=9,step=1)

                extent_dict["up_left"] = st.slider(
                    'Upper left limb',
                    min_value = 0, max_value=9,step=1)

                extent_dict["up_right"] = st.slider(
                    'Upper right limb',
                    min_value = 0, max_value=9,step=1)


                st.markdown("**On a scale of 0-18, select how much area the Eczema is covering the following body parts. The higher the number, the more skin area coverage**")

                extent_dict["lower_left"] = st.slider(
                    'Lower left limb',
                    min_value = 0, max_value=18,step=1)

                extent_dict["lower_right"] = st.slider(
                    'Lower right limb',
                    min_value = 0, max_value=18,step=1)

                extent_dict["ant_trunk"] = st.slider(
                    'Anterior trunk',
                    min_value = 0, max_value=18,step=1)

                extent_dict["back"] = st.slider(
                    'Back',
                    min_value = 0, max_value=18,step=1)


                st.markdown("**On a scale of 0-1, select how much area the Eczema is covering the following body part. The higher the number, the more skin area coverage**")

                extent_dict["genitals"] = st.slider(
                    'Genitals',
                    min_value = 0, max_value=1,step=1)


            with st.expander("Intensity"):

                intensity_dict = {}

                st.markdown("**On a scale of 0-3, select how severe each sign is. The higher the number, the more severe the sign**")

                intensity_dict["redness"] = st.slider(
                'Redness',
                min_value = 0, max_value=3,step=1)

                intensity_dict["swelling"] = st.slider(
                'Swelling',
                min_value = 0, max_value=3,step=1)

                intensity_dict["oozing"] = st.slider(
                'Oozing',
                min_value = 0, max_value=3,step=1)

                intensity_dict["scratch_marks"] = st.slider(
                'Scratch marks',
                min_value = 0, max_value=3,step=1)

                intensity_dict["skin_thicken"] = st.slider(
                'Skin tickening',
                min_value = 0, max_value=3,step=1)

                intensity_dict["dryness"] = st.slider(
                'Dryness',
                min_value = 0, max_value=3,step=1)


            with st.expander("Subjective Symptoms"):

                sub_symp_dict = {}

                st.markdown("**On scale of 0-10, rate your sleep quality. :green[0] is :green[BEST] sleep quality, :red[10] is :red[WORST] sleep quality**")

                sub_symp_dict["sleep_loss"] = st.slider(
                'Sleep loss',
                min_value = 0, max_value=10,step=1)

                #st.write("0 is best sleep quality, 10 is worst sleep quality")


                st.markdown("**On scale of 0-10, rate how severe your itchiness is. :green[0] is :green[no itch], :red[10] is the :red[worst] imaginable itch**")

                sub_symp_dict["itchiness"] = st.slider(
                'Itchiness',
                min_value = 0, max_value=10,step=1)
        

            scorad_dict = {
                "extent" : extent_dict,
                "intensity" : intensity_dict,
                "sub_symp" : sub_symp_dict,
            }

            if st.form_submit_button("Submit"):
                submit_scorad(scorad_dict)
                st.rerun()

    with tab_2:

        with st.container(border = True):

            st.subheader("Past Records")

            uid = st.session_state.user["localId"]
            query = db.collection("scorad").where("uid", "==", uid).get()
            
            temp_list = []

            for i in query:
                temp = list(i.values())[0]
                temp_list.append(temp)

            df = pd.DataFrame(data = temp_list) 
            df = df.drop(columns = ["uid"])
            df = df.loc[:,['date','score']]

            st.dataframe(df, use_container_width=True,)

  
        