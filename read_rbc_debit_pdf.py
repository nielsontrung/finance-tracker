"""Module for parsing transactional data from e-statements"""

import pandas as pd
from pathlib import Path
from re import search
from tika import parser
from read_rbc_pdf import (
    get_month_num,
    has_month,
    is_negative_transaction,
)
from util import get_category


def get_debit_statement_range(path: Path, content: str):
    """_summary_

    Args:
        content (str): _description_

    Returns:
        _type_: _description_
    """
    pattern = r"From (January|February|March|April|May|June|July|August|September|October|November|December)\s(\d{2}),\s{1}(\d{4}) to (January|February|March|April|May|June|July|August|September|October|November|December) (\d{2}), (\d{4})"
    date_range = ()
    try:
        date_range = search(pattern, content).groups()
    except Exception as e:
        print(f"error while processing statement: {path.resolve()} {e}")
    return date_range


def get_account_number(content: str) -> str:
    """get the account number from the e-statement

    Args:
        path (Path): pathlib Path of the e-statement

    Returns:
        str: account number
    """
    pattern = r"(Your account number: )(\d{5}-\d{7})"
    account_number = ""
    account_number = search(pattern, content).group(2)
    return account_number


def get_debit_pdf_content(path, content: str, debug=False) -> str:
    """returns debit transaction from statement content

    Args:
        content (str): statement content

    Returns:
        _type_: _description_
    """
    start_pattern = r"Opening Balance \d+\.\d{2}"
    end_pattern = r"Closing Balance \d+\.\d{2}"
    amount_pattern = r"\d+\.\d{2}"
    month_pattern = r"\b\d{1,2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b"
    content = content.replace(",", "").replace("$", "").strip("\n")
    start_index, end_index = 0, 0
    try:
        start_index = search(start_pattern, content).end()
        end_index = search(end_pattern, content).start()
    except Exception as e:
        return ""
    transaction_content = content[start_index:end_index].strip("\n")
    lines = transaction_content.splitlines()
    transactions = ""
    for i, line in enumerate(lines):
        if debug:
            print(i, line)
        line.lower().replace(",", "").replace("$", "")
        if (
            "your " in line
            or "opening balance" in line
            or ("from" in line and "to" in line)
        ):
            continue
        elif search(month_pattern, line) or search(amount_pattern, line):
            transactions += line + "\n"
    # amount_pattern = r"(.+?)\s\d+\.\d+"
    date = ""
    description = ""
    actual_transactions = []
    transactions = transactions.splitlines()
    for i in range(len(transactions)):
        transaction = transactions[i]
        has_month = search(month_pattern, transaction)
        has_amount = search(amount_pattern, transaction)
        # get date
        if has_month is not None:
            date = has_month.group(0)

        if has_month and has_amount is None:
            description = transaction
            continue

        if has_month and has_amount:
            actual_transactions.append(transaction)
            description = ""

        elif has_month is None and has_amount:
            transaction = f"{description if description else date} {transaction}"
            actual_transactions.append(transaction)
    transaction_content = "\n".join(actual_transactions).lower()
    return transaction_content


def get_content(path: Path) -> str:
    """get the content from statement

    Args:
        path (Path): pathlib Path of the file

    Returns:
        str: returns the content of the statement
    """
    raw = parser.from_file(str(path.resolve()))
    content = raw["content"]
    return content


def valid_transaction(date, line):
    line = line.lower()
    # valid online banking payment
    if "questrade" in line or "u of calg-tuitn" in line:
        return True
    if (
        "item returned" in line
        or "payment received" in line
        or "online banking payment" in line
        or "amex" in line
        or "e-transfer sent humptys" in line
        or "payment rbc credit card" in line
        or "misc payment cibc cpd" in line
        or "opening balance" in line
        or "closing balance" in line
        or "online banking transfer" in line
        or "online transfer" in line
        or "br to br" in line
        or "e-transfer cancel" in line
        or "transfer to deposit account" in line
        or (date == "2020/06/03" and "mobile cheque deposit" in line)
    ):
        return False
    else:
        return True


def get_debit_transactions(path, debug=True, write_file=False):
    """
    Takes a pathlib path that specifies the location of a debit e-statement
    and extracts all transactions from the e-statement to the provided file.

    @params
        path          - Required : path of the debit e-statement (pathlib Path)
        csv           - Required : all_transactions.csv being written to
    @return
        transactions  - list of transactions as csv row
        balances      - dictionary of balances {date:balance}
        amounts       - dictionary of amounts {date:amount}
    """
    # regular expressions
    date_re = r"^(\d{1,2} [a-z]{3})"
    amount_re = r"(\d+\.\d{2})"

    if isinstance(path, Path):
        path = Path(path)
    content = get_content(path)
    if content is None:
        return []
    transaction_content = get_debit_pdf_content(path, content)
    if transaction_content == "":
        return []

    if debug:
        for i in transaction_content.splitlines():
            print(repr(i))
    account_number = get_account_number(content)
    date_range = get_debit_statement_range(path, content)
    year = date_range[2]
    if debug:
        print(date_range)
    lines = transaction_content.splitlines()
    month_abbr, month_num, day, date, description, category = ("",) * 6
    amount_groups, date_groups = (), ()
    amount = 0
    points = 0
    description = ""
    transactions = []
    for line_index, line in enumerate(lines):
        if debug:
            print(line_index, line)
        line_lower = line.lower()
        # get the date
        if search(date_re, line_lower):
            date_groups = search(date_re, line_lower).groups()
            date_groups = date_groups[0].split(" ")
            day = date_groups[0].zfill(2)
            if month_abbr == "dec" and date_groups[1] == "jan":
                year = str(int(year) + 1)
            month_abbr = date_groups[1]
            month_num = get_month_num(month_abbr)
            date = "/".join((year, month_num, day))
            description = line.replace(" ".join(date_groups), "").strip()
        else:
            description = line
        is_valid = valid_transaction(date, line)
        if not is_valid:
            description, category = ("",) * 2
            amount = 0
            continue

        # get transaction amount
        has_amount = search(amount_re, description) is not None
        if has_amount:
            amount_groups = search(amount_re, description).groups()
            amount = float(amount_groups[0])
            description = description[: description.find(str(amount))]
            description = description.strip().replace("-", "")
        category = get_category(description.lower())

        is_negative = is_negative_transaction(category)
        if is_negative:
            amount = -amount

        source_file = str(path.resolve()).replace("\\\\", "\\")
        transaction = (
            account_number,
            date,
            int(year),
            int(month_num),
            int(day),
            category,
            description,
            float(format(amount, ".2f")),
            points,
            source_file,
        )
        transactions.append([*transaction])
        # reset transaction variables
        # description = ""
        amount = 0
        category = ""
        source_file = ""
    if debug:
        for i in transactions:
            print(i)
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


# path = r"C:\Users\Nielson\Documents\Statements\rbc\01259-5555313\2018\Savings Statement-5313-2018-Sep-24.pdf"
# print(path)
# path = Path(path)
# get_debit_transactions(path, debug=True)
