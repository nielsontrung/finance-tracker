"""Module for main application"""

import re
from pathlib import Path
from tika import parser
import pandas as pd
from rename_file import rename_file
from read_rbc_credit_pdf import get_credit_transactions
from read_rbc_debit_pdf import get_debit_transactions
from progressbar import progress_bar


def rename_files():
    """rename files that match the file pattern"""
    file_pattern = r"\d+X+\d+-20\d{2}-\d{2}-\d{2}-20\d{2}-\d{2}-\d{2}.pdf$"
    file_paths = Path(".").rglob("*.pdf")
    files = []

    for path in file_paths:
        if re.search(file_pattern, str(path.name)):
            rename_file(path)
            files.append(path)

    return files


def get_transactions_rbc(folder, files: list, debug=False):
    """process all files

    Args:
        files (list): _description_
    """
    all_transactions = []
    for e_statement in progress_bar(
        files, prefix="Progress:", suffix="Complete", length=50
    ):
        path = e_statement.resolve()
        path = "\\".join(path.parts)
        transactions = []
        if debug:
            print("path:", path, "Visa in content: ", "Visa" in path)
            print(path)
        if "Visa" in path:
            try:
                transactions = get_credit_transactions(e_statement, debug=debug)
            except Exception as e:
                print(f'exception processing credit transactions: "{e_statement}"')
                print(e)
        else:
            try:
                transactions = get_debit_transactions(e_statement, debug=debug)
            except Exception as e:
                print(f'exception processing debit transactions: "{e_statement}"')
                print(e)
        if transactions != []:
            all_transactions.extend(transactions)
    # create csv
    file_name = f"{folder}\\rbc_transactions.csv"
    columns = [
        "account",
        "date",
        "year",
        "month",
        "day",
        "category",
        "description",
        "amount",
        "points",
        "source_file",
    ]
    df = pd.DataFrame(all_transactions, columns=columns)
    df.to_csv(file_name, index=False)
    df.to_csv("./csv/rbc_transactions.csv", index=False)
    print(f'all transactions processed: "{file_name}"')
    return all_transactions
