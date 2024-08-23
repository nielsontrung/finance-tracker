"""Module that runs the main application"""

import json
import os
from pathlib import Path
import pandas as pd
from datetime import datetime

from data import create_data_js
from amex import get_transactions_amex
from cibc import get_transactions_cibc
from rbc import get_transactions_rbc


def clear():
    """clear the console buffer

    Returns:
        _type_: _description_
    """
    return os.system("cls")


def print_options(message, options: list):
    """"""
    print(message)
    for i, option in enumerate(options):
        print(f"\t({i}) {option}")


def get_folder_path():
    """helper function get user input for folder path of rbc e-statements"""
    message = r'(2) Enter the folder path or choose one of the following options below ex) "C:\Documents\Statements"'
    config_json = open("./config.json").read()
    config_json = json.loads(config_json)
    default_folder = config_json.get("rbc").get("folderPath")
    options = [f"default folder: '{default_folder}'", "exit program"]
    print_options(message, options)
    while 1:
        user_input = input().replace('"', "")
        is_dir = os.path.isdir(user_input)
        if is_dir:
            clear()
            return user_input
        elif user_input == "0":
            clear()
            return default_folder
        elif user_input == "1":
            clear()
            exit(0)
        else:
            clear()
            print_options(message, options)


def get_input():
    """Get user input"""
    while 1:
        choice = input()
        if choice in ["0", "1"]:
            clear()
            return choice
        elif choice == "2":
            clear()
            exit(0)
        else:
            clear()
            message = "(1) Choose one of the following options below:"
            options = [
                "exit",
                "recursively process all e statements",
                "process all-transactions.csv",
            ]
            print_options(message, options)


def is_statement(file_name: str, debug=False):
    file_name_lower = file_name.lower()
    match = "statement" in file_name_lower
    if debug:
        print(f"match: {match} {repr(file_name)}")
    if match:
        return True
    else:
        return False


def filter_paths(path):
    """return list of e-statement files"""
    paths = Path(path).rglob("*.pdf")
    paths = [f"{i.resolve()}" for i in paths]
    paths_iterator = filter(is_statement, paths)
    paths = list(paths_iterator)
    paths = [Path(f) for f in paths]
    return paths


def main(debug=False):
    """start the application"""
    output_file = "./csv/all-transactions.csv"
    output_file_headers = [
        "account",
        "date",
        "year",
        "month",
        "day",
        "category",
        "description",
        "amount",
        "points",
        "sourceFile",
    ]
    message = r"(1) Please choose one of the following options below:"
    options = ["recursively parse e-statements", "process all-transactions.csv", "exit"]
    print_options(message, options)
    choice = get_input()
    transactions = []

    # recursively process all e statements/csvs
    if choice == "0":
        # files = rename_files()
        folder = get_folder_path()
        files = filter_paths(folder)

        if len(files) < 1:
            print("could not find any e statements...")
            os.system("pause")
            exit(0)

        rbc_transactions = get_transactions_rbc(folder, files, debug=debug)
        amex_transactions = get_transactions_amex()
        cibc_transactions = get_transactions_cibc()
        transactions.extend(rbc_transactions)
        transactions.extend(amex_transactions)
        transactions.extend(cibc_transactions)
        df = pd.DataFrame(transactions, columns=output_file_headers)
        if debug:
            print(df)
        df = df[df[output_file_headers].notnull().all(1)]
        df = df.sort_values(by=["date"])
        df.to_csv(output_file, index=False)

    # process all-transactions.csv
    elif choice == "1":
        if not os.path.isfile(output_file):
            print("did not find " + output_file)
            os.system("pause")
            exit(0)
        f = open(output_file, "r", encoding="utf-8")
        # lines = f.read().splitlines()

    # prepare data for visualization using eCharts.js and dataTables.js
    create_data_js(output_file)


if __name__ == "__main__":
    main(debug=False)
