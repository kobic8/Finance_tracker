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
    months = ['%02d' % (month) for month in range(1, 13)]
    data_dict = {'month': months}
    categories = ['Alt.payments', 'Const.payments', 'Transportation', 'Medical', 'Housing', 'Personal',
                  'Entertainment', 'Gifts', 'Food', 'Income']
    for category in categories:
        data_dict[category] = [0]*12
    df_month = pd.DataFrame(data_dict)
    df_month = df_month.transpose()
    return df_month


def init_df_log():
    import pandas as pd
    data_dict = {}
    headers = ['Category', 'Amount', 'Item', 'Store', 'Date']
    for col in headers:
        data_dict[col] = []
    df_log = pd.DataFrame(data_dict)
    return df_log


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
        update_file(df_month, df_month, full_path)
    return df_month, df_log


def update_file(data_month, data_log, full_path):
    data_month.to_csv(full_path)
    data_log.to_csv('Data/data_all.csv')


def get_expense(expense_date='', expense_store='supermarket', expense_amount=0, expense_name='item',
                expense_cat='electrics'):
    expense_name = input("what did you buy?")
    expense_cat = input("What category?")
    expense_date = input("Enter purchase date [dd/mm/yyyy]\n")
    expense_store = input("where did you buy it?")
    expense_amount = int(input('How much?'))
    expense = [expense_cat, expense_amount, expense_name, expense_store, expense_date]
    return expense


def add_item_data_log(data_log, expense):
    import pandas as pd
    row_to_add = pd.Series(expense, index=data_log.columns)
    data_log = data_log.append(row_to_add, ignore_index=True)
    return data_log


def add_item_data_month(data, item):
    # TODO change this for by month
    day, month, year = item['Date'].split('/')
    category = item['Category']
    if year in data:
        if month in data[year]:
            if category in data[year][month]:
                data[year][month][category]['Total'] += item['amount']
                data[year][month][category]['Items'].append(item)
            else:
                data[year][month][category] = {}
                data[year][month][category]['Total'] = item['amount']
                data[year][month][category]['Items'] = [item]
        else:
            data = new_item(data, item)
    else:
        data[year] = {}
        data = new_item(data, item)
    return data


def plot_by_cat(data):
    pass


def plot_total(data):
    pass


def export_data(data_for_graph, fullpath):
    df_to_json = {}
    for key, value in data_for_graph.items():
        df_to_json[key] = [str(val) for val in value]
    result = data_for_graph.to_


def new_item(data, item):
    day, month, year = item['Date'].split('/')
    category = item['Category']
    data[year][month] = {}
    data[year][month][category] = {}
    data[year][month][category]['Total'] = item['amount']
    data[year][month][category]['Items'] = [item]
    return data


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    from os import path

    filename = 'fin_data.csv'
    directory = 'Data'
    fullpath = path.join(directory, filename)
    clear = True
    data = init(fullpath, clear)
    data_log = init_df_log()
    get_from_user = False
    while get_from_user:
        item = get_expense()
        data = add_item(data, item)
        proceed = input("Got some more data? [Y/N]")
        if proceed == 'N':
            get_from_user = False
    update_file(data, fullpath)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
