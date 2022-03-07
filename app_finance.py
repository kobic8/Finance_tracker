import streamlit as st
import main_fin_tracker as fin
import pandas as pd

# Text
st.title("Kobic's Finance App")
st.info(f" Last updated: {fin.last_updated('r')}")
# Init
file_month = 'fin_data.csv'
file_log = 'data_all.csv'
directory = 'Data'
clear = False
df_month, df_log = fin.init(directory, [file_month, file_log], clear)
submit_load = st.button("Load data")
if submit_load:
    df_month, df_log = fin.init(directory, [file_month, file_log], clear)
    if not df_log.empty and not df_month.empty:
        st.success("Data is loaded")
st.header("What would you like to do today?")

# action
action = st.radio("Please choose your action", ("Check my balance", "Enter new data"))
# let the user choose what to do: check balance / enter new data?
if action == "Enter new data":
    with st.form("new_data"):
        # submit_cancel = st.form_submit_button("Cancel and exit")
        amount = []
        amount = st.text_input("Enter the amount of purchase")
        if amount:
            amount = int(float(amount))
        name = st.text_input("Enter the name of the purchase")
        store = st.text_input("Where did you buy it?")
        categories = ['Alt.payments', 'Const.payments', 'Transportation', 'Medical', 'Housing', 'Personal',
                      'Entertainment', 'Gifts', 'Food', 'Income']
        category = st.selectbox("select category", categories)
        date = st.date_input("When did you but it?")
        date_str = date.strftime("%d/%m/%Y")
        submit_cancel = st.form_submit_button("Cancel and exit")
        submit_save = st.form_submit_button("save")
        if submit_save:
            print("update the data")
            item = [categories.index(category), category, amount, name, store, date_str]
            # st.dataframe(df_log)
            # st.text(item)
            df_log = fin.add_item_data_log(df_log, item[1:])
            st.text("Please verify the following traffic update")
            st.dataframe(df_log.iloc[-1:])
            check_save = st.checkbox("Data is correct, please update the dataset")
            if check_save:
                saved = False
                day, month, year = item[-1].split('/')
                df_month = fin.add_item_data_month(df_month, item)
                saved = True
                if saved:
                    st.success("Dataset is updated")
                    fin.last_updated('w')
            else:
                df_log = df_log.head(-1)
        # update the data
        st.dataframe(df_log.iloc[-4:])
        st.dataframe(df_month)
        update = fin.update_file([df_month, df_log], directory, [file_month, file_log])
        if update:
            st.success("Dataset files are updated")

if submit_load:
    # --- create data frames for total income/outcome/savings ----
    df_income = df_month.iloc[-1:, df_month.columns != 'Categories']
    df_income.index = ["Income"]  # st.text(df_income.index) # st.dataframe(df_income)
    # reduce monthly df to numbers only, remove first column and last row (income)
    df_num = df_month.iloc[:, df_month.columns != 'Categories']
    df_num = df_num.head(-1)
    # sum all columns to get the total monthly outcome
    df_outcome = df_num.sum().to_frame(name="Outcome").transpose()  # st.dataframe(df_outcome)  st.text(df_outcome.index)
    # Calculate the monthly savings
    nd_savings = df_income.values - df_outcome.values
    df_savings = pd.DataFrame(nd_savings, columns=df_outcome.columns, index=["Savings"])  # st.dataframe(df_savings)
    # create TOTAL dataframe: Income, outcome, savings
    # df_total = df_income.transpose()
    # df_total["Outcome"] = df_outcome.transpose().values
    # df_total["Savings"] = df_savings.transpose().values

    df_total = df_savings.transpose()
    df_total["Outcome"] = df_outcome.transpose().values
    df_total["Income"] = df_income.transpose().values

    df_total.index = ['%02d' % (month) for month in range(1, 13)]  # st.dataframe(df_total)
    # plot graph
    st.bar_chart(df_total)

    # ---- create data frames for total outcome ----
    df_num = df_num.transpose()
    categories = ['Alt.payments', 'Const.payments', 'Transportation', 'Medical', 'Housing', 'Personal', 'Entertainment',
                  'Gifts', 'Food']
    df_num.columns = categories
    df_num.index = df_total.index  # st.dataframe(df_num)
    # plot graph
    st.bar_chart(df_num)

    st.header("Last updated traffic")
    st.dataframe(df_log.iloc[-2:])