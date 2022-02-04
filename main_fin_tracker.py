# This is the main Python script that includes the operating functions for the finance app.

# Press Shift+F10 to execute it independently without streamlit and function from the terminal

def init_df_monthly():
    """
    This function initiates the dataframe object as a monthly table by expense categories:
    Each row stands for each category and each column represents a month.

    Returns
    -------
    df_month: empty dataframe object for a month
    """
    import pandas as pd
    categories = ['Alt.payments', 'Const.payments', 'Transportation', 'Medical', 'Housing', 'Personal',
                  'Entertainment', 'Gifts', 'Food', 'Income']
    months = ['%02d' % (month) for month in range(1, 13)]
    data_dict = {'Categories': categories}
    for month in months:
        data_dict[month] = [0]*10
    df_month = pd.DataFrame(data_dict)
    df_month.to_csv('Data/fin_data.csv', index=False, encoding="utf-8-sig")
    return df_month


def init_df_log():
    """
    This function initiates the dataframe object as a log table of all expenses.
    The headers of the empty table will include: ['Category', 'Amount', 'Item', 'Store', 'Date']

    Returns
    -------
    df_log: empty dataframe object for expenses log
    """
    import pandas as pd
    data_dict = {}
    headers = ['Category', 'Amount', 'Item', 'Store', 'Date']
    for col in headers:
        data_dict[col] = []
    df_log = pd.DataFrame(data_dict)
    df_log.to_csv('Data/data_all.csv', index=False, encoding="utf-8-sig")
    return df_log


def update_file(data, direc, file_list):
    """
    This procedure updates the current data csv files with the new dataframe content.
    Before updating the files, this procedure saves the original files in a backup directory
    Parameters
    ----------
    data      [list] list of the two dataframes: df_month, df_log
    direc     [str] path to the directory to save the output csv files
    file_list [list] list of the two names of the csv files correspond to data month and data_log

    Returns
    -------

    """
    from os import path
    import shutil
    for file, df in zip(file_list, data):
        full_path = path.join(direc, file)
        back_path = path.join(direc + '/Backup', file)
        shutil.copyfile(full_path, back_path)
        df.to_csv(full_path, index=False, encoding="utf-8-sig")
    return True
    # data_log.to_csv('Data/data_all.csv', index=False)


def init(direc, file_list, override=False):
    """
    This functions initiates the two dataframes: month and log when the program starts. If the csv data files already
    exist and override flag is set to FALSE, then the output is the existed data in the files, else new data files
    will be created.
    Parameters
    ----------
    direc     [str] path to the directory to save the output csv files
    file_list [list] list of the two names of the csv files correspond to data month and data_log
    override  [bool] a flag to direct the function if to delete the existing files (and create new ones) or not

    Returns
    -------
    df_month, df_log: dataframes
    """
    from os import path
    import pandas as pd
    data = []
    for file in file_list:
        full_path = path.join(direc, file)
        if path.isfile(full_path) and not override:
            df = pd.read_csv(full_path)
            data.append(df)
    if data:
        df_month, df_log = data
    else:
        df_month = init_df_monthly()
        df_log = init_df_log()
    return df_month, df_log


def get_expense(expense_date='', expense_store='supermarket', expense_amount=0, expense_name='item',
                expense_cat='electrics'):
    """
    This procedure gets input from the user about a specific purchase and returns the collected data in a list.
    Parameters
    ----------
    expense_date   [str] purchase date [dd/mm/yyyy]
    expense_store  [str] the name of the store
    expense_amount [float] the amount of money for the expense
    expense_name   [str] the name of the product
    expense_cat    [str] the category corresponds to the expense.

    Returns
    -------
    a list that consists of all collected data related to the expense.
    """
    expense_name = input("what did you buy?")
    categories = ['Alt.payments', 'Const.payments', 'Transportation', 'Medical', 'Housing', 'Personal',
                  'Entertainment', 'Gifts', 'Food', 'Income']
    print(*enumerate(categories), sep="\n")
    N_cat = int(input("What category? please select the number"))
    expense_cat = categories[N_cat]
    expense_date = input("Enter purchase date [dd/mm/yyyy]\n")
    expense_store = input("where did you buy it?")
    expense_amount = "{:.2f}".format(float(input('How much?')))
    expense = [N_cat, expense_cat, expense_amount, expense_name, expense_store, expense_date]
    return expense


def add_item_data_log(data_log, expense):
    """
    This procedure updates the dataframe 'data_log' by the data given in the 'expense' list.
    Parameters
    ----------
    data_log [pandas dataframe]
    expense  [list] includes all data related to a specific item purchased.

    Returns
    -------
    updated data frame
    """
    import pandas as pd
    indexing = data_log.columns
    if len(expense) != len(data_log.columns):
        indexing = data_log.columns[1:]
    row_to_add = pd.Series(expense, index=indexing)
    data_log = data_log.append(row_to_add, ignore_index=True)
    return data_log


def add_item_data_month(data_month, expense):
    """
    This procedure updates the dataframe 'data_month' by the data given in the 'expense' list.
    Parameters
    ----------
    data_month [pandas dataframe]
    expense  [list] includes all data related to a specific item purchased.

    Returns
    -------
    updated data frame
    """
    day, month, year = expense[-1].split('/')
    # TODO sometimes month appears as '01' and sometimes as '1'
    if month not in data_month.columns:
        month = month.strip('0')
    cell = data_month.at[expense[0], month] # .iloc[Ncat+1, month]
    cell += expense[2]
    data_month.at[expense[0], month] = cell
    return data_month


def plot_by_cat(data_month):
    pass


def plot_total(data):
    pass


if __name__ == '__main__':
    file_month = 'fin_data.csv'
    file_log = 'data_all.csv'
    directory = 'Data'
    clear = False
    df_month, df_log = init(directory, [file_month, file_log], clear)
    get_from_user = False
    while get_from_user:
        item = get_expense()
        df_log = add_item_data_log(df_log, item[1:])
        df_month = add_item_data_month(df_month, item)
        proceed = input("Got some more data? [Y/N]")
        if proceed == 'N':
            get_from_user = False
            print(df_log)
    update_file([df_month, df_log], directory, [file_month, file_log])
    print('Finish')
