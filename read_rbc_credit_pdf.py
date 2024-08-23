"""Module for parsing transcational data from credit card e-statements"""

import pandas as pd
from pathlib import Path
from re import search
from tika import parser
from read_rbc_pdf import get_month_num
from util import get_category


def get_statement_range(path: Path, content: str, debug=False):
    """get the date range from the statement content

    Args:
        content (str): content of the statement

    Returns:
        _type_: return a list of the date range tokenized
    """
    content = content.replace(",", "")
    if debug:
        print(path)
        print(repr(content))
    pattern = r"STATEMENT FROM (JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\s{1}(\d{2})\s{1}TO\s{1}(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\s{1}(\d{2})\s{1}(20\d{2})"
    date_range = search(pattern, content)
    if date_range is None:
        pattern = r"STATEMENT FROM (JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\s{1}(\d{2}) (20\d{2}) TO (JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC) (\d{2}) (\d{4})"
        date_range = search(pattern, content)
    if date_range is not None:
        date_range = date_range.groups()
    if debug:
        print(repr(content))
        print(date_range)
        print(path.resolve(), pattern, date_range)
    return date_range


def get_account_number(content: str) -> str:
    """get the account number from the e-statement

    Args:
        path (Path): pathlib Path of the e-statement

    Returns:
        str: account number
    """
    account_number = ""
    pattern = r"([0-9]{4}\s{1}\d{2}[*]{2}\s{1}[*]{4}\s{1}\d{4})( - PRIMARY)"
    account_number = search(pattern, content)
    if account_number is not None:
        account_number = account_number.group(1)
        return account_number
    pattern = r"\d*\s*\d*\s*\*+\s*\*+\s*\d*"
    account_number = search(pattern, content)
    if account_number is not None:
        account_number = account_number.group(0)
        return account_number
    raise Exception(
        "account number not found using regular expression pattern: {pattern}"
    )


def get_credit_pdf_content(content: str):
    """
    Takes a pathlib path that specifies the location of
    a credit e-statement returns the contents of specified file.

    @params
        path    - Required : path of the debit e-statement (pathlib Path)

    @return
        content - transactions of the debit e-statement
    """
    lines = content.splitlines()
    transaction_pattern = r"^(((jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)|(aug)|(sep)|(oct)|(nov)|(dec))\s{1}\d{1,2}\s{1}){2}.+(\d+\.\d+){1}$"
    month_pattern = r"^(jan)|^(feb)|^(mar)|^(apr)|^(may)|^(jun)|^(jul)|^(aug)|^(sep)|^(oct)|^(nov)|^(dec)"
    id_pattern = r"^\d{3,}$"
    amount_pattern = r"^-?(\d+.\d+)$"
    content = ""
    for line in lines:
        line = line.lower().replace(",", "").replace("$", "")
        if search(transaction_pattern, line):
            continue
        elif (
            search(month_pattern, line)
            or search(id_pattern, line)
            or search(amount_pattern, line)
        ):
            content += line + "\n"
    return content


def get_pdf_content(path):
    """_summary_

    Args:
        path (_type_): _description_

    Returns:
        _type_: _description_
    """
    fname = str(path.parents[0]) + "/" + str(path.name)
    raw = parser.from_file(fname)
    content = raw["content"]
    return content


def get_credit_transactions(path, debug=False, write_file=False) -> list:
    """
    extracts all transactions from the e-statement to the provided a pathlib path that specifies the location of a credit e-statement.

    @params
        path - Required : path of the credit e-statement (pathlib Path)
        csv  - Required : all_transactions.csv being written to
    """
    if isinstance(path, Path):
        path = Path(path)
    content = get_pdf_content(path)
    if content is None:
        return []
    transaction_content = get_credit_pdf_content(content)
    if debug:
        print("content: \n", repr(content))
        print("transaction content: \n", repr(transaction_content))
    account_number = get_account_number(content)
    date_range = get_statement_range(path, content, debug=debug)
    year = date_range[2] if date_range[2].isnumeric() else date_range[-1]
    lines = transaction_content.splitlines()

    # regex patterns to find transaction details
    id_pattern = r"^\d{3,}$"
    amount_pattern = r"^-?(\d+.\d+)$"
    transaction_pattern = r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s(\d{2})\s(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s(\d{2})\s(.*)"
    month_abbr, month_num, day, date, description, category = ("",) * 6
    amount = 0
    source_file = str(path.resolve())
    transactions = []
    for line in lines:
        if search(transaction_pattern, line):
            regex_groups = search(transaction_pattern, line).groups()
            if debug:
                print("groups", regex_groups)
            if month_abbr == "dec" and regex_groups[0] == "jan":
                year = str(int(year) + 1)
            month_abbr = regex_groups[0]
            month_num = get_month_num(regex_groups[0])
            day = regex_groups[1].zfill(2)
            date = "/".join((year, month_num, day))
            description = regex_groups[-1].strip().replace("-", "")
            category = get_category(description)
        elif search(id_pattern, line):
            continue
        elif search(amount_pattern, line):
            amount = -float(line)
        if amount != 0:
            if amount < 0:
                temp = (
                    account_number,
                    date,
                    int(year),
                    int(month_num),
                    int(day),
                    category,
                    description,
                    format(amount, ".2f"),
                    0,
                    source_file,
                )
                transactions.append([*temp])
            date, description, category = ("",) * 3
            amount = 0
    if debug:
        print(transactions)
    if write_file:
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
            "sourceFile",
        ]
        df = pd.DataFrame(transactions, columns=columns)
        df.to_csv(source_file.replace(".pdf", ".csv"))
    return transactions


path = r"C:\Users\Nielson\Documents\Statements\rbc\Visa-6910\2022\Visa Statement-6910 2022-05-12.pdf"
path = Path(path)
transactions = get_credit_transactions(path, debug=False)
for i in transactions:
    print(i)
