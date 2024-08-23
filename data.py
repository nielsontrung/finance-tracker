"""Module for generating transactional data for ECharts and DataTables"""

import calendar
import json
import pandas as pd


CATEGORIES = [
    i.capitalize() for i in list(json.loads(open("./category.json").read()).keys())
]

FILE_PATH = "./app/data"


# DataTable data
def create_data_table_js(data_table: list):
    """create javascript formatted table"""
    filename = f"{FILE_PATH}/table-data.js"
    print(f'creating "{filename}"')
    f = open(f"{filename}", "w", encoding="utf-8")
    f.write(f"var tableData = {data_table}")
    f.close()


# ECharts Data
def get_sankey_chart_data(df):
    # eCharts example https://echarts.apache.org/examples/en/editor.html?c=sankey-energy
    # data https://echarts.apache.org/examples/data/asset/data/energy.json
    expense_categories = [i for i in CATEGORIES if i not in ["deposits"]]
    expense_categories.sort()
    nodes = [{"name": "Deposits"}]
    nodes += [{"name": i.capitalize()} for i in expense_categories]
    nodes += [{"name": "Net Earnings"}]
    nodes += [{"name": "Net Revenue"}]
    nodes += [{"name": "Net Expenses"}]
    df = df[["category", "amount"]]
    df = df.groupby(["category"], as_index=False).sum().sort_values(by=["amount"])
    expenses = df.values.tolist()
    links = []
    total_expenses = -round(df[df["amount"] < 0]["amount"].sum(), 2)
    total_earnings = round(df[df["amount"] > 0]["amount"].sum(), 2)
    total_revenue = round(total_earnings - total_expenses, 2)
    links.extend(
        [
            {
                "source": "Net Earnings",
                "target": "Net Revenue",
                "value": total_revenue,
            },
            {
                "source": "Net Earnings",
                "target": "Net Expenses",
                "value": total_expenses,
            },
        ]
    )
    for i in expenses:
        (
            category,
            amount,
        ) = i
        category = category.capitalize()
        amount = round(amount, 2)
        if amount == 0:
            continue
        if amount < 0:
            links.append(
                {
                    "source": "Net Expenses",
                    "target": category,
                    "value": -amount,
                }
            )
        else:
            links.append(
                {"source": category, "target": "Net Earnings", "value": amount}
            )
    sankey_data = {"nodes": nodes, "links": links}
    sankey_data_str = json.dumps(sankey_data)
    filename = f"{FILE_PATH}/revenue.json"
    print(f'creating "{filename}"')
    with open(f"{filename}", "w") as f:
        f.write(sankey_data_str)
        f.close()
    return sankey_data


def get_bar_chart_data(df, start_year: int, end_year: int):
    """
    Takes a filename that specifies the file with transactions being read and processed

    @params
        df          - Required : pandas dataframe
        start_year  - Required : starting year of transaction history
        end_year    - Required : ending year of transaction history

    @return
        content - transactions of the debit e-statement
    """

    num_years = int((end_year - start_year) + 1)
    categories_sorted = [i.capitalize() for i in CATEGORIES]
    categories_sorted.sort()
    annual_expenses_by_category = {
        i.capitalize(): [0.00] * num_years for i in categories_sorted
    }
    pie_chart_data = {
        category.capitalize(): [0.0] * num_years for category in categories_sorted
    }
    lifetime_expenses_by_category = {category: 0.0 for category in categories_sorted}
    monthly_earnings = [[str(i), [0.00] * 12] for i in range(start_year, end_year + 1)]
    monthly_expenses = [[str(i), [0.00] * 12] for i in range(start_year, end_year + 1)]

    data_table = []
    transactions = df.values.tolist()
    for i, transaction in enumerate(transactions):
        (
            account,
            date,
            year,
            month,
            day,
            category,
            description,
            amount,
            points,
            source_file,
        ) = transaction
        amount = round(float(amount), 2)
        points = round(float(points), 2)
        month_abbreviation = calendar.month_abbr[month]
        id = str(i).zfill(len(str(len(transactions))))
        data_table.append(
            [
                id,
                account,
                date,
                year,
                month_abbreviation,
                category,
                description,
                amount,
                source_file,
            ]
        )
        year_index = year - start_year
        month_index = month - 1
        category = category.capitalize()
        if amount > 0:
            monthly_earnings[year_index][1][month_index] += amount
            annual_expenses_by_category[category][year_index] += amount
        else:
            amount = abs(amount)
            monthly_expenses[year_index][1][month_index] += amount
            annual_expenses_by_category[category][year_index] += amount
            pie_chart_data[category][year_index] += amount
        lifetime_expenses_by_category[category] = round(
            lifetime_expenses_by_category[category] + amount, 2
        )

    # reformat data for eCharts.js
    # pie_chart_data = [[i.capitalize(), pie_chart_data[i]] for i in pie_chart_data]
    pie_chart_data = [
        [i] + [round(j, 2) for j in pie_chart_data[i]] for i in pie_chart_data
    ]
    pie_chart_data = [
        ["Category"] + [str(i) for i in range(start_year, end_year + 1, 1)]
    ] + pie_chart_data
    annual_expenses_by_category = [
        [i, [round(j, 2) for j in annual_expenses_by_category.get(i)]]
        for i in categories_sorted
    ]
    lifetime_expenses_by_category = [
        [i, round(lifetime_expenses_by_category[i], 2)]
        for i in lifetime_expenses_by_category
    ]
    monthly_earnings = [[i[0], [round(j, 2) for j in i[1]]] for i in monthly_earnings]
    monthly_expenses = [[i[0], [round(j, 2) for j in i[1]]] for i in monthly_expenses]

    result = {
        "annual_expenses_by_category": annual_expenses_by_category,
        "data_table": data_table,
        "lifetime_expenses_by_category": lifetime_expenses_by_category,
        "monthly_earnings": monthly_earnings,
        "monthly_expenses": monthly_expenses,
        "pie_chart_data": pie_chart_data,
    }

    return result


def get_line_race_data(data, start_year: int, end_year: int) -> list:
    """_summary_

    Args:
        data     (_type_): data
        start_year  (int): start year
        end_year    (int): end year

    Returns:
        (list): res
    """
    monthly_earnings = data.get("monthly_earnings")
    monthly_expenses = data.get("monthly_expenses")
    time = [
        "/".join((str(year), str(i).zfill(2)))
        for year in range(start_year, end_year + 1)
        for i in range(1, 13)
    ]
    earnings = []
    for i in monthly_earnings:
        earnings += i[1][::-1]
    expenses = []
    for i in monthly_expenses:
        expenses += i[1][::-1]
    res = []
    res.append(["type", "date", "amount"])
    for i, t in enumerate(time):
        res.append(["earnings", t, earnings[i]])
        res.append(["expenses", t, expenses[i]])
    return res


def get_area_chart_data(df):
    data = []
    for i in df.tolist():
        print(i)
    return data


def create_data_js(filename: str):
    """generate stats.js file contains data

    Args:
        filename (str): all transactions filepath
    """
    df = pd.read_csv(filename)
    start_year = df["year"].min()
    end_year = df["year"].max()
    years = (end_year - start_year) + 1
    months_abbrs = [calendar.month_abbr[i] for i in range(1, 13)]
    dates = df["date"].sort_values().unique().tolist()

    data = get_bar_chart_data(df, start_year, end_year)
    annual_expenses_by_category = data.get("annual_expenses_by_category")
    data_table = data.get("data_table")
    lifetime_expenses_by_category = data.get("lifetime_expenses_by_category")
    monthly_earnings = data.get("monthly_earnings")
    monthly_expenses = data.get("monthly_expenses")
    pie_chart_data = data.get("pie_chart_data")
    line_race_data = get_line_race_data(data, start_year=start_year, end_year=end_year)
    sankey_data = get_sankey_chart_data(df)
    categories_sorted = CATEGORIES
    categories_sorted.sort()
    variables = {
        "startYear": start_year,
        "endYear": end_year,
        "years": years,
        "dates": dates,
        "months": months_abbrs,
        "categories": CATEGORIES,
        "categoriesSorted": CATEGORIES,
        "categoricalExpenses": annual_expenses_by_category,
        "lifetimeCategoricalExpenses": lifetime_expenses_by_category,
        "lineRaceData": line_race_data,
        "monthlyEarnings": monthly_earnings,
        "monthlyExpenses": monthly_expenses,
        "pieChartData": pie_chart_data,
        "sankeyData": sankey_data,
    }

    print(pie_chart_data)

    # create data.js
    filename = f"{FILE_PATH}/data.js"
    f = open(f"{filename}", "w", encoding="utf-8")
    print(f'creating "{filename}"')
    for var_name in variables:
        var_value = variables[var_name]
        f.write(f"var {var_name} = {var_value};\n")
    f.close()

    # create table-data.js
    create_data_table_js(data_table)

    return data


# create_data_js(r"./all-transactions.csv")
