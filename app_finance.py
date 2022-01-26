import streamlit as st
import datetime
import main_fin_tracker as fin

# Init
# TODO: read the data from pc

# Text
st.title("Kobic's Finance App")
st.header("What would you like to do today?")

# action
action = st.radio("Please choose your action", ("Check my balance", "Enter new data"))
# let the user choose what to do: check balance / enter new data?
if action == "Enter new data":
    data_continue = True
    with st.form("new_data"):
        amount = st.text_input("Enter the amount of purchase")
        name = st.text_input("Enter the name of the purchase")
        store = st.text_input("Where did you but it?")
        category = st.selectbox("select category", ['Alt.payments', 'Const.payments', 'Transportation', 'Medical',
                                                    'Housing', 'Personal', 'Entertainment', 'Gifts', 'Food', 'Income'])
        date = st.date_input("When did you but it?")
        submit_cancel = st.form_submit_button("Cancel and exit")
        submit_stop = st.form_submit_button("save")
        if submit_stop:
            print("update the data")
            # TODO update the data
# TODO plot the grpahs
            # st.write(f"hello and welcome: {date.strftime('%d/%m/%Y')}")
# year, month, day = date.split('-')
# st.write(f"day is {day} month is {month} and the year: {year}")

# st expander to close the form