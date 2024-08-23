import pandas as pd
import numpy as np
import json
from datetime import datetime
from util import get_category


def get_transactions_cibc(debug=False):
    config = open("./config.json").read()
    input_file = json.loads(config).get("cibc").get("folderPath")
    df = pd.read_csv(
        input_file,
        names=["date", "description", "amount", "payment", "account"],
        index_col=False,
    )
    df["points"] = 0.0
    df[["year", "month", "day"]] = df["date"].str.split("-", expand=True)
    df["date"] = df["year"] + "/" + df["month"] + "/" + df["day"]
    df["description"] = df["description"].str.replace("-", "")
    df["category"] = df["description"].str.lower()
    df["category"] = df["category"].apply(get_category)
    df["amount"] *= -1
    df["amount"] = df["amount"].replace({np.nan: None})
    df = df[df["amount"].notnull()]
    df["sourceFile"] = input_file
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
    if debug:
        print(df)
    output_folder = "\\".join(input_file.split("\\")[:-1])
    output_file = f"{output_folder}\\cibc_all_transactions.csv"
    print(f'{datetime.now()} saving all cibc transactions: "{output_file}"')
    df.to_csv(output_file, index=False)
    df.to_csv("./csv/cibc_all_transactions.csv", index=False)
    transactions = df.values.tolist()
    return transactions
