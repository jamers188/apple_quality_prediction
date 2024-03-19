import streamlit as st
from PIL import Image
import sqlite3 
import re
import pandas as pd
import pickle

st.set_page_config(page_title="Crop Recommendation", page_icon="https://www.flaticon.com/free-icon/apple_2779430?term=apple+check&page=1&position=9&origin=search&related_id=2779430", layout="centered", initial_sidebar_state="auto", menu_items=None)

def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''
        
    st.markdown(
          f"""
          <style>
          .stApp {{
              background: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSEv-zU7IgfqGSHn46c8XnJARMEllyLfQvLhg&usqp=CAU");
              background-size: cover
          }}
          </style>
          """,
          unsafe_allow_html=True
      )
set_bg_hack_url()

conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(FirstName TEXT,LastName TEXT,Mobile TEXT,City TEXT,Email TEXT,password TEXT,Cpassword TEXT)')
def add_userdata(FirstName,LastName,Mobile,City,Email,password,Cpassword):
    c.execute('INSERT INTO userstable(FirstName,LastName,Mobile,City,Email,password,Cpassword) VALUES (?,?,?,?,?,?,?)',(FirstName,LastName,Mobile,City,Email,password,Cpassword))
    conn.commit()
def login_user(Email,password):
    c.execute('SELECT * FROM userstable WHERE Email =? AND password = ?',(Email,password))
    data = c.fetchall()
    return data
def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data
def delete_user(Email):
    c.execute("DELETE FROM userstable WHERE Email="+"'"+Email+"'")
    conn.commit()

st.title("Welcome to Apple Qulity Check System")

menu=st.sidebar.selectbox("Menu",["Home","Signup","Login","ContactUs"])

if menu=="Home":
    st.write("Welcome to Homepage")
    
if menu=="Signup":
    f_name=st.text_input("First Name")
    l_name=st.text_input("Last Name")
    m_name=st.text_input("Mobile Number")
    c_name=st.text_input("City")
    Email=st.text_input("Email")
    psw=st.text_input("Password",type="password")
    cpsw=st.text_input("Confirm Password",type="password")
    if st.button("Signup"):
        pattern=re.compile("(0|91)?[7-9][0-9]{9}")
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if psw==cpsw:
            if (pattern.match(m_name)):
                if re.fullmatch(regex, Email):
                    create_usertable()
                    add_userdata(f_name,l_name,m_name,c_name,Email,psw,cpsw)
                    st.success("SignUp Success")
                    st.info("Go to Logic Section for Login")
                else:
                    st.warning("Not Valid Email")         
            else:
                st.warning("Not Valid Mobile Number")
        else:
            st.warning("Pass Does Not Match")
    
    
    
    
    
if menu=="Login":
    Email=st.sidebar.text_input("Email")
    Password=st.sidebar.text_input("Password",type="password")
    if st.sidebar.checkbox("Login"):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, Email):
            if Email=='a@a.com' and Password=='123':
                st.success("Logged In as {}".format("Admin"))
                Email=st.text_input("Delete Email")
                if st.button('Delete'):
                    delete_user(Email)
                user_result = view_all_users()
                clean_db = pd.DataFrame(user_result,columns=["FirstName","LastName","Mobile","City","Email","password","Cpassword"])
                st.dataframe(clean_db)
            else:
                result = login_user(Email,Password)
                if result:
                    st.success("Logged In as {}".format(Email))
                    menu2 = ["SVM","KNN","NB","DT","RF","ET"]
                    choice2 = st.selectbox("Select ML",menu2)

                    
                    Size=float(st.slider('Size Value', -5, 10))
                    Weight=float(st.slider('Weight Value', -5, 10))
                    Sweetness=float(st.slider('Sweetness Value', -10, 10))
                    Crunchiness=float(st.slider('Crunchiness Value', -10, 10))
                    Juiciness=float(st.slider('Juiciness Value', -10, 10))
                    Ripness=float(st.slider('Ripness Value', -5, 5))
                    Acidity=float(st.slider('Acidity Value', 0, 14))
                    model=pickle.load(open("model_apple_all.pkl","rb"))
                    mydata=[Size,Weight,Sweetness,Crunchiness,Juiciness,Ripness,Acidity]                  
                    if st.button("Predict"):
                        if choice2=="SVM":
                            prd=model[0].predict([mydata])[0]
                            st.success(prd)
                        if choice2=="KNN":
                            prd=model[1].predict([mydata])[0]
                            st.success(prd)
                        if choice2=="NB":
                            prd=model[2].predict([mydata])[0]
                            st.success(prd)
                        if choice2=="DT":
                            prd=model[3].predict([mydata])[0]
                            st.success(prd)
                        if choice2=="RF":
                            prd=model[4].predict([mydata])[0]
                            st.success(prd)
                        if choice2=="ET":
                            prd=model[5].predict([mydata])[0]
                            st.success(prd)
                    
                    
                
                else:
                    st.warning("Incorrect Email/Password")
        else:
            st.warning("Not Valid Email")
    
    
if menu=="ContactUs":
    #img=Image.open("")
    #st.image(imag,width=200)
    st.write("Name")
    st.write("Mobile")
    st.write("Email")
