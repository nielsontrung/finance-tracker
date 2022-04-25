import os
import calendar

months = [calendar.month_abbr[i] for i in range(1, 13)]

months_dict = {calendar.month_abbr[i]: "-" +
                str(i).zfill(2) + "-" for i in range(1, 13)}

CHEQUINGS_ACCOUNT = "1234XXXXXX5678"
SAVINGS_ACCOUNT = "1234XXXXXX5678"
CREDIT_ACCOUNT = "1234XXXXXX5678"

def get_statement_start_period(file):
    file = file.replace('.pdf', '')
    tokens = file.split('-')
    year, month, date = [int(i) for i in tokens]
    if(month == 1):
        year -= 1
        month = 12
    else:
        month -= 1
    year = str(year)
    month = str(month).zfill(2)
    return '-'.join((year, month, date))


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
        if file.find("Credit Card Statement") != -1:
            new_file_name = file.replace(
                "Credit Card Statement-1234", CREDIT_ACCOUNT)
        elif file.find("Chequing Statement") != -1:
            new_file_name = file.replace(
                "Chequing Statement-1234", CHEQUINGS_ACCOUNT)
        elif file.find("Savings Statement") != -1:
            new_file_name = file.replace(
                "Savings Statement-1234", SAVINGS_ACCOUNT)
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
