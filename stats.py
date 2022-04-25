import calendar

CATEGORIES = [
    'automotive', 'clothing', 'education', 'electronics',
    'entertainment', 'e transfers', 'fine', 'gas', 'general',
    'government', 'groceries', 'healthcare', 'home', 'investments',
    'loans', 'mobile', 'personal care', 'restaurants', 'travel',
    'utilities', 'withdrawal', 'deposit', 'other'
]


def make_table_data_js(data_table: list):
    f = open("table-data.js", "w")
    f.write('var tableData = {}'.format(str(data_table)))
    f.close()


def get_stats(filename: str, start_year: int, end_year: int):
    """
    Takes a filename that specifies the file with transactions being 
    read and processed

    @params
        filename    - Required : csv file being processed which contains transaction history
        start_year  - Required : starting year of transaction history
        end_year    - Required : ending year of transaction history

    @return
        content - transactions of the debit e-statement
    """
    data_table = []
    years = (end_year - start_year) + 1
    categorical_expenses = {category: [0.0] * years for category in CATEGORIES}
    lifetime_categorical_expenses = {category: 0.0 for category in CATEGORIES}
    monthly_earnings = [[str(i), [0.00]*12]
                        for i in range(start_year, end_year + 1)]
    monthly_expenses = [[str(i), [0.00]*12]
                        for i in range(start_year, end_year + 1)]

    with open(filename, "r") as f:
        lines = f.read().splitlines()
        for index, line in enumerate(lines):
            if index == 0:
                continue
            transaction = line.split(', ')
            data_table.append(transaction)
            id, account, date, year, month, description, category, amount = transaction
            year, month, day = [int(i) for i in date.split('/')]
            amount = round(float(amount), 2)
            if amount > 0:
                monthly_earnings[year - start_year][1][-month] += amount
            else:
                amount = abs(amount)
                monthly_expenses[year - start_year][1][-month] += amount
            categorical_expenses[category][year - start_year] += amount
            lifetime_categorical_expenses[category] += amount

    make_table_data_js(data_table)

    # reformat data for eCharts.js
    categorical_expenses = [
        [i] + [round(j, 2) for j in categorical_expenses[i]] for i in categorical_expenses]

    lifetime_categorical_expenses = [[i, round(
        lifetime_categorical_expenses[i], 2)] for i in lifetime_categorical_expenses]

    monthly_earnings = [[i[0], [round(j, 2) for j in i[1]]]
                        for i in monthly_earnings]

    monthly_expenses = [[i[0], [round(j, 2) for j in i[1]]]
                        for i in monthly_expenses]

    categorical_stats = (categorical_expenses, lifetime_categorical_expenses)
    monthly_stats = (monthly_earnings, monthly_expenses)
    result = categorical_stats + monthly_stats
    return result


def get_line_race_data(stats, start_year: int, end_year: int):
    monthly_earnings = stats[2]
    monthly_expenses = stats[3]
    time = ["/".join((str(year), str(i).zfill(2)))
            for year in range(start_year, end_year + 1) for i in range(1, 13)]
    earnings = []
    for i in monthly_earnings:
        earnings += i[1][::-1]
    expenses = []
    for i in monthly_expenses:
        expenses += i[1][::-1]
    res = []
    res.append(['type', 'date', 'amount'])
    for i in range(len(time)):
        res.append(["earnings", time[i], earnings[i]])
        res.append(["expenses", time[i], expenses[i]])
    return res


def write_variable(file, var, position):
    variables = ["startYear", "endYear", "years", "months", "categories", "categoricalExpenses",
                 "lifetimeCategoricalExpenses", "monthlyEarnings", "monthlyExpenses", "lineRaceData"]
    file.write("var {} = {}; ".format(variables[position], str(var)))


def make_stats_js(filename: str, start_year: int, end_year: int):
    years = (end_year - start_year) + 1
    months = [calendar.month_abbr[i] for i in range(1, 13)]
    stats = get_stats(filename, start_year, end_year)
    line_race_data = get_line_race_data(stats, start_year, end_year)
    variables = [start_year, end_year, years, months, CATEGORIES,
                 stats[0], stats[1], stats[2], stats[3], line_race_data]
    f = open("stats.js", 'w')
    for i, var in enumerate(variables):
        write_variable(f, var, i)
    f.close()
