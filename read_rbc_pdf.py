import json
from re import search

# TODO update statement_details to a enum/class


def get_statement_details(fname, debug=False):
    """
    Return details about the e-statement using the filename
    @params
        fname - Required : e-statement filename
    @return
        account     - account number
        year        - e-statement year
        start_month - e-statement start month
        end_month   - e-statement end month
        start_date  - e-statement start date
        end_date    - e-statement end date
    """
    if debug:
        print(fname)
    start_month, end_month, start_date, end_date = ("",) * 4
    details = fname.replace(".pdf", "").split("-")
    account = details[0]
    year = details[1]
    # start_month = details[2]
    # start_date = "-".join((year, start_month, details[3]))
    # end_month = details[5]
    # end_date = "-".join((year, end_month, details[6]))
    return [account, year, start_month, end_month, start_date, end_date]


def get_month_num(month):
    """
    Takes the name of a month returns its numerical value
    @params
        month - Required : name of the month
    @return
        num   - number of the month as a string
    """
    months = {
        "jan": "01",
        "feb": "02",
        "mar": "03",
        "apr": "04",
        "may": "05",
        "jun": "06",
        "jul": "07",
        "aug": "08",
        "sep": "09",
        "oct": "10",
        "nov": "11",
        "dec": "12",
    }

    return months[month]


def get_month_name(month):
    """
    Takes the number of a month as a string and returns the name of the month
    @params
        month - Required : number of the month
    @return
        name  - name of the month as a string
    """
    months = {
        "01": "jan",
        "02": "feb",
        "03": "mar",
        "04": "apr",
        "05": "may",
        "06": "jun",
        "07": "jul",
        "08": "aug",
        "09": "sep",
        "10": "oct",
        "11": "nov",
        "12": "dec",
    }
    return months[month]


def has_month(line):
    """
    Returns bool if line has a month
    @params
        line - Required : line in being parsed

    @return
        bool - True if line has a month in it False if line does not have a month in it
    """
    line = line.lower()
    months = [
        " jan ",
        " feb ",
        " mar ",
        " apr ",
        " may ",
        " jun ",
        " jul ",
        " aug ",
        " sep ",
        " oct ",
        " nov ",
        " dec ",
    ]
    for month in months:
        if month in line:
            return True
    return False


def is_negative_transaction(description):
    """
    Returns bool if the description is a withdrawal
    @params
        description - Required : transaction description

    @return
        bool - True if the description is a withdrawal False if the description is not a withdrawal
    """
    # purchases are always negative
    description = description.lower()
    if "received" in description:
        return False
    positive_transaction = [
        "deposit",
        "e-transfer received",
        "e transfer received",
        "government",
    ]
    for i in positive_transaction:
        if i == description:
            return False
    return True


def valid_transaction(description):
    """
    Returns bool if the description is a valid transaction
    @params
        description - Required : transaction description

    @return
        bool - False if the description contains a string in not_valid
    """
    description = description.lower()
    not_valid = [
        "online banking transfer",
        "online transfer",
        "e-transfer cancel",
        "e-transfer sent humptys",
        "fee",
        "multiproduct rebate",
        "e-transfer sent humptys",
        "withdrawal",
        "item returned unpaid",
    ]
    for i in not_valid:
        if i in description:
            return False
    return True
