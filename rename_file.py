import os

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

months_dict = {
    "Jan": "-01-",
    "Feb": "-02-",
    "Mar": "-03-",
    "Apr": "-04-",
    "May": "-05-",
    "Jun": "-06-",
    "Jul": "-07-",
    "Aug": "-08-",
    "Sep": "-09-",
    "Oct": "-10-",
    "Nov": "-11-",
    "Dec": "-12-"
}


def get_statement_start_period(file):
    file = file.replace('.pdf', '')
    tokens = file.split('-')
    year = int(tokens[1])
    month = int(tokens[2])
    date = tokens[3]
    if(month == 1):
        year -= 1
        month = 12
    else:
        month -= 1
    year = str(year)
    month = str(month)
    if(len(month) < 2):
        month = month.zfill(2)
    statement_start_period = '-'.join((year, month, date))
    return statement_start_period


def rename_file(path):
    parent = path.parents[0]
    file_name = str(path.name)
    new_file_name = file_name
    for month in months:
        if file_name.find(month) != -1:
            new_file_name = file_name.replace(month, months_dict[month])
            os.rename(str(parent) + '\\' + str(file_name),
                      str(parent) + '\\' + new_file_name)


def rename_files(path):
    file_names = os.listdir(path)  # return a list of files in a given path
    for file_name in file_names:
        rename_file(file_name)


def main():
    file_path = input("Please enter the path of your e statements: ")
    files = os.listdir(file_path)
    filtered_files = []
    for file in files:
        new_file_name = ""
        if file.find("Credit Card Statement-6910") != -1:
            new_file_name = file.replace(
                "Credit Card Statement-6910", "451029XXXXXX6910")
        elif file.find("Chequing Statement-1666") != -1:
            new_file_name = file.replace(
                "Chequing Statement-1666", "01259XXX1666")
        elif file.find("Savings Statement-5313") != -1:
            new_file_name = file.replace(
                "Savings Statement-5313", "01259XXX5313")
        for month in months:
            if file.find(month) != -1:
                new_file_name = new_file_name.replace(
                    "-" + month + "-", months_dict[month])
                statement_start_period = get_statement_start_period(
                    new_file_name)
                new_file_name = new_file_name[0:new_file_name.find(
                    '-')] + "-" + statement_start_period + new_file_name[new_file_name.find('-'):len(new_file_name)]
                filtered_files.append(new_file_name)
                os.rename('\\'.join((file_path, file)),
                          '\\'.join((file_path, new_file_name)))
