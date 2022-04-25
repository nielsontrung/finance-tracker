import os
import csv
from re import search
from rename_file import rename_file
from read_credit_pdf import write_credit_transactions
from read_debit_pdf import write_debit_transactions
from pathlib import Path
from progressbar import progressBar
from stats import make_stats_js

ALL_TRANSACTIONS_CSV = 'all-transactions.csv'
CSV_HEADER = 'id, account, date, year, month, description, category, amount \n'


def print_options():
    print("Choose one of the following options below:")
    print("\t(0) exit")
    print("\t(1) recursively process all e statements")
    print("\t(2) process all-transactions.csv")


def get_input():
    def clear(): return os.system('cls')
    while(1):
        choice = input()
        if choice == '1' or choice == '2':
            clear()
            return choice
        elif choice == '0':
            clear()
            exit(0)
        else:
            clear()
            print_options()


def rename_files():
    file_pattern = '\d+X+\d+-20\d{2}-\d{2}-\d{2}-20\d{2}-\d{2}-\d{2}.pdf$'
    file_paths = Path('.').rglob('*.pdf')
    files = []

    for path in file_paths:
        if search(file_pattern, str(path.name)):
            rename_file(path)
            files.append(path)

    return files


def add_transaction_id():
    with open(ALL_TRANSACTIONS_CSV) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_data = ''
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                transaction = tuple(row[1:])
                csv_data += ",".join((str(line_count),) + transaction)+'\n'
                line_count += 1
        f = open(ALL_TRANSACTIONS_CSV, 'w')
        f.write(CSV_HEADER)
        f.write(csv_data)
        f.close()


def get_all_transaction(e_statements):
    all_transactions_csv = open(ALL_TRANSACTIONS_CSV, 'w')
    all_transactions_csv.write(CSV_HEADER)
    for e_statement in progressBar(e_statements, prefix='Progress:', suffix='Complete', length=50):
        if len(e_statement.name) == 38:
            write_debit_transactions(e_statement, all_transactions_csv)
        if len(e_statement.name) == 42:
            write_credit_transactions(e_statement, all_transactions_csv)
    all_transactions_csv.close()


def main():
    print_options()
    choice = get_input()
    start_year, end_year = 0, 0

    # recursively process all e statements
    if choice == '1':
        files = rename_files()

        if len(files) < 1:
            print('could not find any e statements...')
            os.system("pause")
            exit(0)

        start_year = int(files[0].name.split('-')[1])
        end_year = int(files[len(files)-1].name.split('-')[1])
        years = []

        for i in range(start_year, end_year + 1):
            years.append(i)

        get_all_transaction(files)
        add_transaction_id()

    # process all-transactions.csv
    elif choice == '2':
        if not os.path.isfile(ALL_TRANSACTIONS_CSV):
            print('did not find ' + ALL_TRANSACTIONS_CSV)
            os.system("pause")
            exit(0)
        f = open(ALL_TRANSACTIONS_CSV, 'r')
        lines = f.read().splitlines()
        start_year = int(lines[1].split(", ")[3])
        end_year = int(lines[-1].split(", ")[3])

    # prepare data for visualization using eCharts.js and dataTables.js
    make_stats_js(ALL_TRANSACTIONS_CSV, start_year, end_year)


if __name__ == '__main__':
    main()
