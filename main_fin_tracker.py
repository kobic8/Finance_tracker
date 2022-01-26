# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd


def init_df_monthly():
    '''
    This function initiates the data object as a monthly table by expense categories:
    Each row is for each category and each column in set per month.
    -------
    data-frame object
    '''
    import pandas as pd
    categories = ['Alt.payments', 'Const.payments', 'Transportation', 'Medical', 'Housing', 'Personal',
                  'Entertainment', 'Gifts', 'Food', 'Income']
    months = ['%02d' % (month) for month in range(1, 13)]
    data_dict = {'Categories': categories}
    for month in months:
        data_dict[month] = [0]*10
    df_month = pd.DataFrame(data_dict)
    df_month.to_csv('Data/fin_data.csv', index=False)
    return df_month


def init_df_log():
    import pandas as pd
    data_dict = {}
    headers = ['Category', 'Amount', 'Item', 'Store', 'Date']
    for col in headers:
        data_dict[col] = []
    df_log = pd.DataFrame(data_dict)
    df_log.to_csv('Data/data_all.csv', index=False)
    return df_log


def update_file(data_month, data_log, full_path):
    data_month.to_csv(full_path, index=False)
    data_log.to_csv('Data/data_all.csv', index=False)


def init(full_path, override=False):
    '''
    This function initiated the data object: If there is already an existing csv file, the program will load it and
    override it, else it will create an empty csv file.
    Returns
    -------
    data csv file
    '''
    import pandas as pd
    if path.isfile(full_path) and not override:
        df_month = pd.read_csv(full_path)
        df_log = pd.read_csv('Data/data_all.csv')
    else:
        df_month = init_df_monthly()
        df_log = init_df_log()
        # update_file(df_month, df_log, full_path)
    return df_month, df_log


def get_expense(expense_date='', expense_store='supermarket', expense_amount=0, expense_name='item',
                expense_cat='electrics'):
    expense_name = input("what did you buy?")
    categories = ['Alt.payments', 'Const.payments', 'Transportation', 'Medical', 'Housing', 'Personal',
                  'Entertainment', 'Gifts', 'Food', 'Income']
    print(*enumerate(categories), sep="\n")
    N_cat = int(input("What category? please select the number"))
    expense_cat = categories[N_cat]
    expense_date = input("Enter purchase date [dd/mm/yyyy]\n")
    expense_store = input("where did you buy it?")
    expense_amount = int(input('How much?'))
    expense = [N_cat, expense_cat, expense_amount, expense_name, expense_store, expense_date]
    return expense


def add_item_data_log(data_log, expense):
    import pandas as pd
    indexing = data_log.columns
    if len(expense) != len(data_log.columns):
        indexing = data_log.columns[1:]
    row_to_add = pd.Series(expense, index=indexing)
    data_log = data_log.append(row_to_add, ignore_index=True)
    return data_log


def add_item_data_month(data_month, expense):
    day, month, year = expense[-1].split('/')
    cell = data_month.at[expense[0], month] # .iloc[Ncat+1, month]
    cell += expense[2]
    data_month.at[expense[0], month] = cell
    return data_month


def plot_by_cat(data_month):
    pass


def plot_total(data):
    pass


if __name__ == '__main__':
    from os import path

    filename = 'fin_data.csv'
    directory = 'Data'
    fullpath = path.join(directory, filename)
    clear = False
    df_month, df_log = init(fullpath, clear)
    get_from_user = True
    while get_from_user:
        item = get_expense()
        df_log = add_item_data_log(df_log, item[1:])
        df_month = add_item_data_month(df_month, item)
        proceed = input("Got some more data? [Y/N]")
        if proceed == 'N':
            get_from_user = False
            print(df_log)
    update_file(df_month, df_log, fullpath)
    print('Finish')



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
