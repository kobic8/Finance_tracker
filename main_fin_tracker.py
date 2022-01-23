# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def init(full_path, override=False):
    '''
    This function initiated the data object: If there is already an existing json file, the program will load it and
    override it, else it will create an empty json file.
    Returns
    -------
    data json file
    '''
    import json
    data = {}
    if path.isfile(full_path) and not override:
        f = open(full_path)
        data = json.load(f)
    return data


def update_file(data, full_path):
    import json
    with open(full_path, "w") as outfile:
        json.dump(data, outfile, indent=4)


def get_expense(expense_date='', expense_store='supermarket', expense_amount=0, expense_name='item',
                expense_cat='electrics'):
    expense_name = input("what did you buy?")
    expense_cat = input("What category?")
    expense_date = input("Enter purchase date [dd/mm/yyyy]\n")
    expense_store = input("where did you buy it?")
    expense_amount = int(input('How much?'))
    expense = {'amount': expense_amount, 'Category': expense_cat, 'Date': expense_date,
               'Details': {'Name': expense_name, 'Store': expense_store},
               }
    return expense


def new_item(data, item):
    day, month, year = item['Date'].split('/')
    category = item['Category']
    data[year][month] = {}
    data[year][month][category] = {}
    data[year][month][category]['Total'] = item['amount']
    data[year][month][category]['Items'] = [item]
    return data


def add_item(data, item):
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


def init_data_pd():
    import pandas as pd
    months = ['%02d' % (month) for month in range(1, 13)]
    data_for_pd = {'month': months}
    categories = ['Alt.payments', 'Const.payments', 'Transportation', 'Medical', 'Housing', 'Personal',
                  'Entertainment', 'Gifts', 'Food', 'Income']
    for category in categories:
        data_for_pd[category] = [0]*12
    return data_for_pd


def plot_by_cat(data):
    pass


def plot_total(data):
    pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    from os import path

    filename = 'fin_data.json'
    directory = 'Data'
    fullpath = path.join(directory, filename)
    print_hi('PyCharm')
    clear = False
    data = init(fullpath, clear)
    get_from_user = False
    while get_from_user:
        item = get_expense()
        data = add_item(data, item)
        proceed = input("Got some more data? [Y/N]")
        if proceed == 'N':
            get_from_user = False
    update_file(data, fullpath)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
