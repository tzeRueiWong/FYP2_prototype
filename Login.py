import streamlit as st
import firebase

from firebase_key import the_class


firebaseConfig = the_class.firebaseConfig

app = firebase.initialize_app(firebaseConfig)
auth = app.auth()


def register_func(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)

        st.success('Account created sucessfully')
        st.info('Please Login using your email and password')
    except:
        st.warning("Error: Duplicate Email, or password must be at least 6 characters")


def login_func(email, password):
    
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        login_success = True
    except: 
        login_success = False


    if login_success:
        st.success('Logged in successfully')
        st.session_state.user = user
        st.rerun()
    else:
        st.warning('Login Failed')


def logout_func():
    st.session_state.user = ''



if 'user' not in st.session_state:
    st.session_state.user = ''



st.title("Eczema Generative AI")

if st.session_state.user == '':

    login_tab, register_tab = st.tabs(["Login", "Register"])
    
    with login_tab:
        with st.form("login form"):
            
            email = st.text_input('Email Address', key = 'login_email')
            password = st.text_input('Password', type = 'password', key = 'login_password')
            
            
            if st.form_submit_button("Login"):
                login_func(email,password)
                #st.rerun()
                
                
    
    with register_tab:
        with st.form("register form"):
            email = st.text_input('Email Address', key = 'register_email')
            password = st.text_input('Password', type = 'password', key = 'register_password')
            
            if st.form_submit_button('Register'):
                register_func(email, password)

    

else:
    st.success('Logged in as ' + st.session_state.user['email'])
    st.button('logout',on_click=logout_func)

