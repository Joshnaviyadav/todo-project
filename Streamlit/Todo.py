import streamlit as st
import requests
import datetime
from datetime import date
import pandas as pd
st.set_page_config(layout="wide")

local_host = 'http://localhost:8000/'

session_state = st.session_state

def get_jwt_token(username, password):
    
    url = local_host + 'api/token/'
    data = {
        'username': username,
        'password': password
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        token = response.json()
        access_token = token['access']
        return access_token
    else:
        return None
    

def get_data(token):
    url = local_host + 'data/'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return token
    else:
        return None

if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    
    st.markdown("<h1 style='text-align: center; '>LOGIN</h1> <br>", unsafe_allow_html=True)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.write("")
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        col1, col2 ,col3= st.columns(3)
        with col2:
            login_button = st.button("Login")

    if login_button:
        token = get_jwt_token(username, password)
        
        if token:
            data = get_data(token)
            
            if data:
                st.session_state['logged_in'] = True
                st.session_state['token'] = token
                st.session_state['username'] = username
                st.experimental_rerun()
            else:
                 st.write("You do not have permission to access the next page")

        else:
            st.error("Invalid username or password.")
if 'logged_in' in st.session_state and st.session_state['logged_in']:

    token = st.session_state['token']  
    UserName = st.session_state['username']
    st.markdown("<h1 style='text-align: center; '>TODO application</h1> <br>", unsafe_allow_html=True)

    menu = ["Create","Read","Update","Delete","About"]
    choice = st.sidebar.selectbox("MENU",menu)
    
    params={
                    "userName":UserName,
                    "task":None,
                    "createdDate":None,
                    "discription":""
                }    
    
    
    if choice == "Create":
        st.subheader("Add Items")
        with st.form("My Form"):
            # Add form input elements
            col1, col2 = st.columns(2)
            with col1:
                task = st.text_area("Task to do")
            with col2:
                # a,b = st.columns(2)
                task_status = st.selectbox("Status", ["Todo", "Doing", "Done"])
                # with b:
                task_created_date = st.date_input("Start Date")
            file = st.file_uploader("Please choose a file")
            submitted = st.form_submit_button("Add Task")
            if submitted:
                # Perform actions to add task to the todo list
                # Save the task details in the database or any storage
                # Display a success message
                
                if task:
                    url = local_host + "todo/?type=create"
                    headers = {'Authorization': f'Bearer {token}'}
                    params={
                        "userName":UserName,
                        "task":task,
                        "createdDate":task_created_date,
                        "discription":None
                    }
                    response = requests.get(url,headers=headers,params=params)
                    # st.experimental_rerun()
                    if response.status_code == 200:
                        st.success(f"Successfully added task: {task}")
                        
                    else:
                        st.error("You dont have permission to create the task")

    elif choice == "Read":
        st.subheader("View Items")
        url = local_host + "todo/?type=read"
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url,headers=headers,params=params)
        if response.status_code == 200:
            data = response.json()
            task = data['task']
            datee = data['createdDate']
            
            for i in range(len(task)):
                st.write(f'{task[i]},date:{datee[i]}')
        
        else:
            st.error(f'Error: {response.status_code}')
        # Perform actions to fetch and display tasks from the todo list
        # Retrieve task details from the database or any storage
        # Display the tasks in a table or any desired format

    elif choice == "Update":
        st.subheader("Update Items")
        url = local_host + "todo/?type=read"
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)

            selected_data = st.selectbox("Select data:", options=df["task"])
            st.subheader("Update Items")
            url = local_host + "todo/?type=read"
            headers = {'Authorization': f'Bearer {token}'}
            data = {
                "task":selected_data,
            }
            response = requests.get(url, headers=headers,json=data)
            if response.status_code == 200:
                data = response.json()
                task = data['task']
                discrition = data['discription']
                date_list = data['createdDate']
                task = st.text_input("Task to do",task[0])
                discrition = st.text_area("Discription",discrition[0])
                st.write(date[0])
                # print(type(date[0]))
                default_date_str = date_list[0]  # Select the desired date from the list

                # Convert the string to a datetime.date object
                # default_date = datetime.strptime(default_date_str, "%Y-%m-%d").date()
                # Convert start_date and end_date strings to datetime objects
                # start_date = datetime.strptime(start_date, "%Y-%m-%d")
                # createdDate = st.date_input("Created Date", default_date)
                # createdDate = st.date_input("Created Date",date[0])
            # filtered_df = df[df["task"].isin(selected_data)]

        else:
            st.error(f'Error: {response.status_code}')
            

    elif choice == "Delete":
        
        st.subheader("Delete Items")
        url = local_host + "todo/?type=read"
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)

            selected_data = st.multiselect("Select data:", df["task"])

            filtered_df = df[df["task"].isin(selected_data)]

            st.table(filtered_df)

            if st.button("Delete Selected"):
                delete_url = local_host + "todo/?type=delete"
                delete_data = {"tasks": selected_data}
                # print(selected_data)
                # print(delete_data)
                delete_response = requests.get(delete_url, headers=headers, json=delete_data)

                if delete_response.status_code == 200:
                    st.success("Selected items deleted successfully!")
                    st.experimental_rerun()
                else:
                    st.error("An error occurred while deleting the items.")
                # Perform actions to delete tasks from the todo list
                # Delete task details from the database or any storage based on user input
                # Display a success message after deleting the task
                
            
            
        else:
            st.error(f'Error: {response.status_code}')

    elif choice == "About":
        st.subheader("About")
        st.write("This is a simple TODO app built with Streamlit.")
        st.write("It allows you to create, read, update, and delete tasks in your TODO list.")
