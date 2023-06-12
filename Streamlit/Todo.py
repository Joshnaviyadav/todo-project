# import streamlit as st
# import requests
# from datetime import date

# st.set_page_config(layout="wide")

# local_host = 'http://localhost:8000/'

# session_state = st.session_state

# def get_jwt_token(username, password):
#     url = local_host + 'api/token/'
#     data = {
#         'username': username,
#         'password': password
#     }

#     response = requests.post(url, data=data)

#     if response.status_code == 200:
#         token = response.json()
#         access_token = token['access']
#         return access_token
#     else:
#         return None
    

# def get_data(token):
#     url = local_host + 'data/'
#     headers = {'Authorization': f'Bearer {token}'}
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         return token
#     else:
#         return None


# if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
#     st.markdown("<h1 style='text-align: center; '>Login</h1> <br>", unsafe_allow_html=True)
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.write("")
#     with col2:
#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")
#         col1, col2, col3, col4, col5 = st.columns(5)
#         with col3:
#             login_button = st.button("Login")

#     if login_button:
#         token = get_jwt_token(username, password)
#         if token:
#             data = get_data(token)
#             if data:
#                 st.session_state['logged_in'] = True
#                 st.session_state['token'] = token
#                 st.experimental_rerun()
#             else:
#                 st.write("You dont have permission to access the next page")
#         else:
#             st.error("Invalid username or password.")

# # Check if the user is logged in and retrieve the token from the session state
# if 'logged_in' in st.session_state and st.session_state['logged_in']:
#     token = st.session_state['token']
#     st.markdown("<h1 style='text-align: center; '>Todo List</h1> <br>", unsafe_allow_html=True)
#     tab_container = st.empty()
#     selected_tab = st.sidebar.radio("Select an animal", ["Add", "todo"])

#     if selected_tab == "todo":
#         st.header("todo")
#         url = local_host + "todo/"
#         # headers = {'Authorization': f'Bearer {token}'}
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             title = data['title']
#             details = data['details']
#             datee = data['date']
            
#             for i in range(len(title)):
#                 st.write(f'{title[i]},date:{datee[i]}')
        
#         else:
#             st.error(f'Error: {response.status_code}')
                
#         # show the added lits here from data base by sending get request to url
#     elif selected_tab == "Add":
        
#         default_date = date.today()
#         title = st.text_input("Title", value="")
#         details = st.text_area("Details", value="")
#         date = st.date_input("Date",  min_value=default_date)
#         submit = st.button("Submit")
        
#         if submit:
#             pass
#             # earise the data entered and
#             #send the data through url as post request
#             #save the details in data base show it in todo list
            

#     # Adjust the width of the sidebar
#     st.markdown(
#         """
#         <style>
#         .sidebar .sidebar-content {
#             width: 100px;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )   


#     #create todo list 
#     #show the data fetching from data base and also if the task is completed the details list needs to appear and also create session for it

#     # import streamlit as st

#     # def redirect_to_another_app():
#     #     # Add the script path for your other Streamlit app
#     #     st.experimental_rerun("app.py")

#     # # Your code for the current Streamlit app continues here
#     # st.write("This is the current Streamlit app")

#     # if st.button("Go to Another App"):
#     #     redirect_to_another_app()


import streamlit as st
import requests
import datetime

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
                st.experimental_rerun()
            else:
                 st.write("You do not have permission to access the next page")

        else:
            st.error("Invalid username or password.")
if 'logged_in' in st.session_state and st.session_state['logged_in']:

    token=st.session_state['token']    
    st.markdown("<h1 style='text-align: center; '>TODO application</h1> <br>", unsafe_allow_html=True)

    menu = ["Create","Read","Update","Delete","About"]
    choice = st.sidebar.selectbox("MENU",menu)
    
    if choice == "Create":
        st.subheader("Add Items")
        col1, col2 = st.columns(2)
        with col1:
            task = st.text_area("Task to do")
        with col2:
            task_status = st.selectbox("Status", ["Todo", "Doing", "Done"])
            task_due_date = st.date_input("Due Date")
        file = st.file_uploader("Please choose a file")
        
        if st.button("Add Task"):
            # Perform actions to add task to the todo list
            # Save the task details in the database or any storage
            # Display a success message
            st.success(f"Successfully added task: {task}")

    elif choice == "Read":
        st.subheader("View Items")
        # Perform actions to fetch and display tasks from the todo list
        # Retrieve task details from the database or any storage
        # Display the tasks in a table or any desired format

    elif choice == "Update":
        st.subheader("Update Items")
        # Perform actions to update tasks in the todo list
        # Update task details in the database or any storage based on user input
        # Display a success message after updating the task

    elif choice == "Delete":
        st.subheader("Delete Items")
        # Perform actions to delete tasks from the todo list
        # Delete task details from the database or any storage based on user input
        # Display a success message after deleting the task

    elif choice == "About":
        st.subheader("About")
        st.write("This is a simple TODO app built with Streamlit.")
        st.write("It allows you to create, read, update, and delete tasks in your TODO list.")
