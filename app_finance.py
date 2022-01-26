import streamlit as st
import datetime
import main_fin_tracker as fin
import pandas as pd

# Text
st.title("Kobic's Finance App")
# Init
# TODO: read the data from pc
submit_load = st.button("Load data")
if submit_load:
    file_month = 'fin_data.csv'
    file_log = 'data_all.csv'
    directory = 'Data'
    clear = False
    df_month, df_log = fin.init(directory, [file_month, file_log], clear)
    if not(df_log.empty) and not(df_month.empty):
        st.success("Data is loaded")
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
# st.dataframe(df_month.iloc[:, df_month.columns != 'Categories'])
df_income = df_month.iloc[-1:, df_month.columns != 'Categories']
df_income.index = ["Income"]
st.text(df_income.index)
st.dataframe(df_income)

df_num = df_month.iloc[:, df_month.columns != 'Categories']

df_num = df_num.head(-1)

df_outcome = df_num.sum().to_frame(name="Outcome").transpose()
st.dataframe(df_outcome)
st.text(df_outcome.index)

nd_savings = df_income.values - df_outcome.values
df_savings = pd.DataFrame(nd_savings, columns=df_outcome.columns, index=["Savings"])
st.dataframe(df_savings)

df_total = df_income.transpose()
# df_total = df_total.append(df_outcome.transpose())
# df_total = df_total.append(df_savings.transpose())
df_total["Outcome"] = df_outcome.transpose().values
df_total["Savings"] = df_savings.transpose().values
df_total.index = ['%02d' % (month) for month in range(1, 13)]
st.dataframe(df_total)

# st.text(df_savings)
st.bar_chart(df_total)
st.text(df_total.columns)

df_num = df_num.transpose()
# df_num.columns = df_month.iloc[:, df_month.columns == 'Categories']
categories = ['Alt.payments', 'Const.payments', 'Transportation', 'Medical', 'Housing', 'Personal',
                  'Entertainment', 'Gifts', 'Food']
df_num.columns = categories
st.dataframe(df_num)


st.bar_chart(df_num)
# TODO create total outcome-income chart
            # st.write(f"hello and welcome: {date.strftime('%d/%m/%Y')}")
# year, month, day = date.split('-')
# st.write(f"day is {day} month is {month} and the year: {year}")

# st expander to close the form