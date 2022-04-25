from tika import parser
from re import search
from read_pdf import get_statement_details, get_month_num, get_category


def get_credit_pdf_content(path):
    """
    Takes a pathlib path that specifies the location of 
    a credit e-statement returns the contents of specified file.

    @params
        path    - Required : path of the debit e-statement (pathlib Path)

    @return
        content - transactions of the debit e-statement
    """
    fname = str(path.parents[0]) + '/' + str(path.name)
    raw = parser.from_file(fname)
    lines = raw['content'].splitlines()
    transaction_pattern = "^(((jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)|(aug)|(sep)|(oct)|(nov)|(dec))\s{1}\d{1,2}\s{1}){2}.+(\d+\.\d+){1}$"
    month_pattern = '^(jan)|^(feb)|^(mar)|^(apr)|^(may)|^(jun)|^(jul)|^(aug)|^(sep)|^(oct)|^(nov)|^(dec)'
    id_pattern = "^\d{3,}$"
    amount_pattern = "^-?(\d+.\d+)$"
    content = ''
    for line in lines:
        line = line.lower().replace(',', '').replace('$', '')
        if search(transaction_pattern, line):
            continue
        elif search(month_pattern, line) or search(id_pattern, line) or search(amount_pattern, line):
            content += line + '\n'
    return content

# get all transactions from credit e-statement


def write_credit_transactions(path, csv):
    """
    Takes a pathlib path that specifies the location of a credit e-statement 
    and extracts all transactions from the e-statement to the provided file.

    @params
        path          - Required : path of the credit e-statement (pathlib Path)
        csv           - Required : all_transactions.csv being written to
    """
    content = get_credit_pdf_content(path)
    if content is None:
        return
    f_name = str(path.name)
    lines = content.splitlines()
    statement_details = get_statement_details(f_name)

    # regex patterns to find transaction details
    id_pattern = "^\d{3,}$"
    month_pattern = '(((jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)|(aug)|(sep)|(oct)|(nov)|(dec))\s{1}\d{1,2}\s{1}){2}'
    amount_pattern = "^-?(\d+.\d+)$"

    account_number = statement_details[0]
    year = statement_details[1]
    month_name, month_num, day, id, date, description, category, transaction = (
        '',) * 8
    amount = 0

    for line in lines:
        tokens = line.split(' ')
        if search(month_pattern, line):
            month_name = tokens[0]
            month_num = get_month_num(month_name)
            day = tokens[1]
            if statement_details[2] == "12" and month_num == "01":
                date = '/'.join((str(int(year) + 1), month_num, day))
            else:
                date = '/'.join((year, month_num, day))
            for i in tokens[4:]:
                description += i + ' '
            description = description[:-1]
            category = get_category(description)
        elif search(id_pattern, line):
            id = line
        elif search(amount_pattern, line):
            amount = -float(line)
        if amount != 0:
            if amount < 0:
                transaction = ', '.join(
                    (id, account_number, date, year, month_num, description, category, format(amount, '.2f'))) + '\n'
                csv.write(transaction)
            id, date, description, category, transaction = ('',) * 5
            amount = 0
