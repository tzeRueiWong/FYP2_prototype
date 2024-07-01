import streamlit as st
import firebase

from firebase_key import the_class


firebaseConfig = the_class.firebaseConfig
app = firebase.initialize_app(firebaseConfig)
db = app.firestore()

def add_item(table, input):

    if input == "":
        return

    uid = st.session_state.user['localId']
    data = {"uid":uid, "name":input}
    db.collection(table).add(data)
    st.toast("Added", icon="✅")

def remove_item(table, row_id):
    db.collection(table).document(row_id).delete()
    st.toast("Removed", icon="❗")

def get_content(table):
    
    uid = st.session_state.user["localId"]
    query = db.collection(table).where("uid", "==", uid).get()

    return query


if 'user' not in st.session_state:
    st.session_state.user = ''


if st.session_state.user == '':
    st.warning("Please log in to continue")
    
else:

    st.title("Triggers")

    allergen_tab, irritant_tab = st.tabs(["Allergen", "Irritant"])

    with allergen_tab:
        with st.form("Allergen Form"):
                    
            allergen = st.text_input('Enter an allergen:')
            
            if st.form_submit_button("Add Allergen"):
                add_item("allergens", allergen)
            
        with st.container(border=True):

            data = get_content("allergens")
                
            if len(data) == 0:
                st.text("No allergens recorded")
            else:
                st.text("Recorded Allergens:")

            for i in data:         

                col_1, col_2 = st.columns(2)
                with col_1:
                    st.text(list(i.values())[0]["name"])
                
                with col_2:
                    st.button("Remove", key = list(i.keys())[0], on_click = remove_item, args = ["allergens", list(i.keys())[0]])

    with irritant_tab:
        with st.form("Irritant Form"):
                    
            irritant = st.text_input('Enter an irritant:')
            
            if st.form_submit_button("Add Irritant"):
                add_item("irritants", irritant)
            
        with st.container(border=True):
                
            data = get_content("irritants")

            if len(data) == 0:
                st.text("No irritants recorded")
            else:
                st.text("Recorded Irritants:")

            for i in data:
                col_1, col_2 = st.columns(2)
                with col_1:
                    st.text(list(i.values())[0]["name"])
                
                with col_2:
                    st.button("Remove", key = list(i.keys())[0], on_click = remove_item , args = ["irritants", list(i.keys())[0]])

    
   
