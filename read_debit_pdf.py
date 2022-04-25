import uuid
from tika import parser
from re import search
from read_pdf import get_statement_details, get_month_num, has_month, is_withdrawal, valid_transaction, get_category


def get_debit_pdf_content(path):
    """
    Takes a pathlib path that specifies the location of 
    a debit e-statement returns the contents of specified file.

    @params
        path  - Required : path of the debit e-statement (pathlib Path)

    @return
        content - transactions of the debit e-statement
    """
    fname = str(path.parents[0]) + '/' + str(path.name)
    raw = parser.from_file(fname)
    lines = raw['content'].splitlines()
    pattern = "\d+\.\d+$"
    content = ''
    for line in lines:
        line = line.lower().replace(',', '').replace('$', '')
        if 'your ' in line:
            continue
        elif has_month(line) or search(pattern, line):
            content += line + '\n'
    return content


def write_debit_transactions(path, csv_file):
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
    content = get_debit_pdf_content(path)

    if len(content) == 0:
        return None

    f_name = str(path.name)
    lines = content.splitlines()
    statement_details = get_statement_details(f_name)

    amount_pattern = "\d+\.\d+$"

    account_number = statement_details[0]
    year = statement_details[1]

    month_num, day, id, date, description, category, transaction = ('',) * 7
    amount = 0

    for line in lines:

        if 'opening balance' in line or 'closing balance' in line:
            continue
        tokens = line.split(' ')
        # get the date
        if tokens[0].isnumeric() and len(tokens[0]) <= 2:
            day = tokens[0]
            month_num = get_month_num(tokens[1])
            if len(day) < 2:
                day = '0' + day
            # get the description
            for i in range(2, len(tokens)):
                if search(amount_pattern, tokens[i]) is None:
                    description += tokens[i] + ' '
        else:
            if search(amount_pattern, line) is not None:
                for tok in tokens:
                    if search(amount_pattern, tok) is None:
                        description += tok + ' '
        if search(amount_pattern, line) is None:
            continue
        # if no balance multiple transaction's on transaction date
        if search(amount_pattern, tokens[len(tokens)-2]) is None:
            amount = float(tokens[len(tokens)-1])
        else:
            amount = float(tokens[len(tokens)-2])
        id = str(uuid.uuid4())
        if statement_details[2] == "12" and month_num == "01":
            date = '/'.join((str(int(year) + 1), month_num, day))
        else:
            date = '/'.join((year, month_num, day))
        description = description.strip()
        category = get_category(description)

        # skip invalid transactions
        if (date == '2020/06/03' and 'mobile cheque deposit' in description):
            continue
        # determine if amount is positive or negative
        amount = abs(amount)
        if 'purchase' in description or is_withdrawal(category):
            amount = -amount

        transaction = ', '.join(
            (id, account_number, date, year, month_num, description, category, format(amount, '.2f'))) + '\n'
        # online banking transfer transactions are payments
        # to credit accounts will not be included in the csv
        # fees and monthly rebates will not be included
        if valid_transaction(description):
            csv_file.write(transaction)
        # reset variables after every transaction
        id, date, description, category, transaction = ('',) * 5
        amount = 0
