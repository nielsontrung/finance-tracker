import pandas as pd
import json
import os
from datetime import datetime
from util import get_category


def get_ofx_transaction():
    config = open("./config.json").read()
    input_file = json.loads(config).get("amex").get("filepath")
    df = pd.read_csv(
        input_file,
        names=["date", "id", "amount", "description", "foreignAmount", "points"],
        index_col=False,
    )
    df = df[~df["description"].str.contains("PAYMENT")]
    df["amount"] = df["amount"].abs()
    df["amount"] *= -1
    df["foreignAmount"] = df["foreignAmount"].fillna(0)
    df["points"] = df["points"].fillna(0)
    df[["month", "day", "year"]] = df["date"].str.split("/", expand=True)
    df["date"] = df["year"] + "/" + df["month"] + "/" + df["day"]
    df["id"] = df["id"].str.replace("Reference: ", "")
    df["account"] = "Amex"
    df["description"] = df["description"].str.lower()
    df["description"] = df["description"].str.replace("-", "")
    df["category"] = df["description"].apply(get_category)
    df["sourceFile"] = input_file
    df = df.drop("foreignAmount", axis=1)
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
    df = df[columns]
    transactions = df.values.tolist()
    return transactions


def get_year_summary_amex():
    config = json.loads(open("./config.json").read()).get("amex")
    ofx = config.get("filepath")
    folder_path = config.get("folderPath")
    csv_files = os.listdir(folder_path)
    csv_files = [
        f"{folder_path}\\{i}"
        for i in csv_files
        if ".csv" in i and "Year End Summary" in i
    ]
    print(csv_files)
    dfs = []
    for i in csv_files:
        df = pd.read_csv(
            i,
            index_col=False,
        )
        df["SourceFile"] = i
        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)
    rename_dict = {
        "Account Number": "account",
        "Date": "date",
        "Month-Billed": "month",
        "Category": "category",
        "Transaction": "description",
        "Charges $": "amount",
        "Credits $": "points",
        "SourceFile": "sourceFile",
    }
    df = df.rename(columns=rename_dict)
    df = df.dropna(subset=["month", "description", "amount"], how="any")
    df = df[~df["description"].str.contains("PAYMENT")]
    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y").dt.strftime("%Y/%m/%d")
    df["year"] = pd.to_datetime(df["date"], format="%Y/%m/%d").dt.year
    df["month"] = pd.to_datetime(df["date"], format="%Y/%m/%d").dt.month
    df["day"] = pd.to_datetime(df["date"], format="%Y/%m/%d").dt.day
    df["category"] = df["description"].apply(get_category)
    df["amount"] = df["amount"].str.replace(",", "")
    df["amount"] = df["amount"].str.replace(" ", "0.00")
    df["amount"] = -pd.to_numeric(df["amount"])
    df = df[df["amount"] < 0.00]
    df["amount"] = df["amount"].fillna(0.00)
    df["points"] = df["points"].str.replace(" ", "0.00")
    df["points"] = pd.to_numeric(df["points"])
    df["points"] = df["points"].fillna(0.00)
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
    df = df[columns]
    transactions = df.values.tolist()
    # for i in transactions:
    #     print(i)
    return transactions


def get_transactions_amex():
    config = json.loads(open("./config.json").read()).get("amex")
    ofx_transactions = get_ofx_transaction()
    year_summary_transactions = get_year_summary_amex()
    transactions = ofx_transactions + year_summary_transactions
    headers = [
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
    df = pd.DataFrame(transactions, columns=headers)
    output_folder = config.get("folderPath")
    output_file = f"{output_folder}\\amex_all_transactions.csv"
    print(f'{datetime.now()} saving all amex transactions: "{output_file}"')
    df.to_csv(output_file, index=False)
    df.to_csv("./csv/amex_all_transactions.csv", index=False)
    return transactions


# get_ofx_transaction()
# get_year_summary_amex()
# get_transactions_amex()
